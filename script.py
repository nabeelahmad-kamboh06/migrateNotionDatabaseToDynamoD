import os
import boto3
import requests

# 🔐 Load from environment or set directly
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "YOUR_NOTION_INTEGRATION_TOKEN")
NOTION_DATABASE_ID = "YOUR_NOTION_DATABASE_ID"
DYNAMODB_TABLE = "Rockstar"

# 🧾 Notion API endpoint
NOTION_API_URL = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 📦 AWS DynamoDB client
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(DYNAMODB_TABLE)

def extract_plain_text(prop):
    """Extract plain_text from title or rich_text fields."""
    if prop.get("type") == "title":
        return "".join(t.get("plain_text", "") for t in prop.get("title", []))
    if prop.get("type") == "rich_text":
        return "".join(t.get("plain_text", "") for t in prop.get("rich_text", []))
    return ""

def fetch_notion_pages():
    results = []
    has_more = True
    next_cursor = None

    while has_more:
        payload = {}
        if next_cursor:
            payload["start_cursor"] = next_cursor

        res = requests.post(NOTION_API_URL, headers=HEADERS, json=payload)
        res.raise_for_status()
        data = res.json()

        results.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        next_cursor = data.get("next_cursor")

    return results

def sync_to_dynamodb(pages):
    for page in pages:
        props = page.get("properties", {})
        seller_id = extract_plain_text(props.get("RockstarSellerId", {}))

        if not seller_id:
            print(f"❌ Skipping page {page['id']} (missing RockstarSellerId)")
            continue

        item = {
            "RockstarSellerId": seller_id,
            "RockstarId": extract_plain_text(props.get("RockstarId", {})),
            "RockstarMpId": extract_plain_text(props.get("RockstarMpId", {})),
        }

        try:
            table.put_item(Item=item)
            print(f"✅ Inserted: {seller_id}")
        except Exception as e:
            print(f"❌ Error inserting {seller_id}: {e}")

if __name__ == "__main__":
    notion_pages = fetch_notion_pages()
    sync_to_dynamodb(notion_pages)

# 🚀 Notion to DynamoDB Sync Script

This Python script fetches data from a Notion database and populates an AWS DynamoDB table named `Rockstar`. It is designed specifically for Notion pages with the following properties:

- `RockstarSellerId` (used as DynamoDB Partition Key `SellerId`)
- `RockstarId` (Notion title field)
- `RockstarMpId` (optional rich text field)

---

## 📦 Requirements

- Python 3.7+
- AWS credentials with permission to write to DynamoDB
- A Notion integration with read access to your target database
- An existing DynamoDB table called `Rockstar` with:
  - Partition Key: `SellerId` (String)

---

## 🔧 Setup

### 1. Clone the Repository or Copy the Script

Save the Python script as `notion_to_dynamodb.py`.

### 2. Install Dependencies

```bash
pip install boto3 requests

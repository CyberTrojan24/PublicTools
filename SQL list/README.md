# SQL List 💉

A powerful CLI tool for exploring and learning about SQL injection techniques, designed for educational purposes and authorized testing.

## ✨ Features

- 🔍 Browse different categories of SQL injections
- 📚 View detailed explanations of each technique
- 📋 Copy payloads directly to clipboard
- 🎨 Interactive shell interface with colored output

## 🚀 Getting Started

1. Launch the program:
   ```bash
   python main.py
   ```

2. Use these commands in the SQL shell:

   | Command | Description |
   |---------|-------------|
   | `list` | Show all SQL injection categories |
   | `show <category>` | List all injections in a category |
   | `get <category> <number> [-explain]` | Copy injection to clipboard |
   | `help` | Display available commands |
   | `exit` | Exit the program |

## 📑 Available Categories

- 🔐 Authentication Bypass
- 🔄 Union Based
- ⚠️ Error Based
- ⏱️ Time Based

## 💡 Example Usage

### 1. List Categories
```sql
sql> list
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Available SQL Injection Categories ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Category              │ Count     │
├─────────────────────┼──────────┤
│ Authentication Bypass│    6     │
│ Union Based         │    5     │
│ Error Based         │    4     │
│ Time Based          │    5     │
└─────────────────────┴──────────┘
```

### 2. Show Category Injections
```sql
sql> show authentication bypass
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Injections for Authentication Bypass ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ # │ Payload                    │
│ 1 │ ' OR '1'='1               │
│ 2 │ ' OR '1'='1' --           │
│ ...                           │
└───┴───────────────────────────┘
```

### 3. Get Injection with Explanation
```sql
sql> get authentication bypass 1 -explain
╔══════════════════════════╗
║    Copied to clipboard   ║
╚══════════════════════════╝
Payload: ' OR '1'='1

📝 Explanation:
This injection creates a condition that's always true by making '1'='1'.
It bypasses login by making the WHERE clause always evaluate to true.
```

## ⚠️ Security Notice
This tool is intended for **educational purposes** and **authorized testing only**. Do not use these injections on systems without explicit permission.

## 🔧 Requirements
- Python 3.6 or higher
- Required packages:
  ```
  pyperclip>=1.8.2
  rich>=13.0.0
  ```

---
Created with 💙 by Cyber Trojan LLC

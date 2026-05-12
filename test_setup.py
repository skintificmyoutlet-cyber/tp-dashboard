"""
快速测试脚本 - 验证Google Sheets API配置
运行此脚本确保API配置正确
"""
import sys
import os

def test_credentials():
    print("=" * 50)
    print("Google Sheets API Configuration Test")
    print("=" * 50)

    # 检查credentials.json
    if not os.path.exists('credentials.json'):
        print("[ERROR] credentials.json not found")
        print("\nPlease follow these steps:")
        print("1. Visit https://console.cloud.google.com/")
        print("2. Create project -> Enable Google Sheets API")
        print("3. Create OAuth 2.0 credentials (Desktop app)")
        print("4. Download JSON file, rename to credentials.json")
        print("5. Put it in current directory")
        return False

    print("[OK] Found credentials.json")

    # 测试导入
    try:
        from google_sheets_reader import GoogleSheetsReader
        print("[OK] Successfully imported GoogleSheetsReader")
    except ImportError as e:
        print(f"[ERROR] Import failed: {e}")
        print("\nPlease install dependencies: pip install -r requirements.txt")
        return False

    # 测试连接
    try:
        print("\nConnecting to Google Sheets API...")
        print("(First run will open browser for authorization)")
        reader = GoogleSheetsReader()
        print("[OK] API connection successful!")

        # 测试读取数据
        print("\nTesting FB-ID data reading...")
        df = reader.get_fb_data('ID')
        if not df.empty:
            print(f"[OK] Successfully read {len(df)} rows")
            print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
        else:
            print("[WARNING] Data is empty, please check sheet content")

        return True

    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_credentials()

    if success:
        print("\n" + "=" * 50)
        print("[SUCCESS] Configuration complete! Now you can run:")
        print("   streamlit run app.py")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("[FAILED] Please fix the issues above")
        print("=" * 50)
        sys.exit(1)

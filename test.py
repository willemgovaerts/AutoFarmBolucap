from datetime import datetime, timezone

if __name__ == "__main__":
    print("test")
    with open('/tmp/file.tx'
              't', 'a+') as file_object:
        file_object.write(f"New line time = {datetime.now(timezone.utc)}\n")
print("test")
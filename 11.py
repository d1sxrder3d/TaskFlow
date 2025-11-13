from datetime import datetime, timedelta, timezone

data1 = datetime.utcnow()

data2 = datetime.utcnow() + timedelta(minutes=15)

if __name__ == "__main__":
    print(data1)
    print(data2)
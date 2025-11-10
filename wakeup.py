import threading, time, requests

def keep_alive():
    while True:
        try:
            requests.get("https://mylivenews.streamlit.app/")  # or your public URL
            print("requested")
        except Exception:
            pass
        time.sleep(300)  # every 5 minutes

threading.Thread(target=keep_alive, daemon=True).start()

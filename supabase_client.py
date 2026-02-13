try:
  from supabase import create_client, Client

  SUPABASE_URL = "https://fwwfgwnqrnchjizyzzhd.supabase.co"
  SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3M6ZSI6ImFub24iLCJpYXQiOjE3NzA5NDg1NjAsImV4cCI6MjA4NjUyNDU2MH0.uKtpcmqQaJBzAM80LwVUT84G4V8pglyRY3VcUGuiwoQ"

  supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
  print(f"Error importing supabase: {e}")
  supabase = None

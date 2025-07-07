from supabase import create_client, Client
import os

SUPABASE_URL = "https://qjjancckzcwhqjddfzys.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFqamFuY2NremN3aHFqZGRmenlzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA3ODEzMjUsImV4cCI6MjA2NjM1NzMyNX0.YdXu6ErZ0PfCpjvQkAy2Q0kJ2Y-00IBn0agMDzPp3gw"
DATABASE_URL = "postgresql://postgres:Pdc!!123@db.ehgnkwmrtbfwzzebvvqm.supabase.co:5432/postgres"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY,DATABASE_URL)

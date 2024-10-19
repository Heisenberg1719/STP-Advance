# Fetch Admin Username Based on Phone Number
fetch_admin_query = """
    SELECT admin_username 
    FROM master 
    WHERE admin_phone_number = %s
"""

# Fetch User Username Based on Phone Number
fetch_user_query = """
    SELECT username 
    FROM user_demographics 
    WHERE phone_number = %s
"""

# Query to authenticate an admin by retrieving their hashed password
authenticate_admin_query = """
    SELECT admin_password AS password 
    FROM master 
    WHERE admin_username = %s
"""

# Query to authenticate a user by retrieving their hashed password
authenticate_user_query = """
    SELECT hashed_password AS password 
    FROM user_demographics 
    WHERE username = %s
"""

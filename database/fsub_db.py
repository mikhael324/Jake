#Mikhael
import motor.motor_asyncio
from info import FSUB_CHANNEL_1, FSUB_CHANNEL_2, DATABASE_URI_1

class Fsub_DB:
    def __init__(self):
        if DATABASE_URI:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
            self.db = self.client["Fsub_DB"]
            self.col1 = self.db[str(FSUB_CHANNEL_1)]
            self.col2 = self.db[str(FSUB_CHANNEL_2)]
        else:
            self.client = None
            self.db = None
            self.col1 = None
            self.col2 = None

    def isActive(self):
        return self.client is not None

    async def add_user(self, id, name, username, date, channel=None):
        try:
            if channel == 1:
                await self.col1.insert_one({'id': id, 'name': name, 'username': username, 'date': date})
            elif channel == 2:
                await self.col2.insert_one({'id': id, 'name': name, 'username': username, 'date': date})
        except Exception as e:
            print(f"Error adding user: {e}")

    async def get_user(self, id, channel=None):
        try:
            if channel == 1:
                return await self.col1.find_one({'id': int(id)})
            elif channel == 2:
                return await self.col2.find_one({'id': int(id)})
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None

    async def get_all_users(self, channel=None):
        try:
            if channel == 1:
                return self.col1.find({})
            elif channel == 2:
                return self.col2.find({})
        except Exception as e:
            print(f"Error retrieving all users: {e}")
            return None

    async def purge_user(self, id, channel=None):
        try:
            if channel == 1:
                await self.col1.delete_one({'id': int(id)})
            elif channel == 2:
                await self.col2.delete_one({'id': int(id)})
        except Exception as e:
            print(f"Error deleting user: {e}")

    async def purge_all_users(self, channel=None):
        try:
            if channel == 1:
                await self.col1.delete_many({})
            elif channel == 2:
                await self.col2.delete_many({})
        except Exception as e:
            print(f"Error purging all users: {e}")

    async def total_users(self, channel=None):
        try:
            if channel == 1:
                return await self.col1.count_documents({})
            elif channel == 2:
                return await self.col2.count_documents({})
        except Exception as e:
            print(f"Error counting users: {e}")
            return 0
    

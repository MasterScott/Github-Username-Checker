import random, string, aiohttp, asyncio
from colorama import *
init()

"""
Some variables for our async start.
"""
loop = asyncio.ProactorEventLoop()
asyncio.set_event_loop(loop)



class Github:
    def __init__(self):
        self.length = 3 # This is the length of the username to generate, change this to what ever you would like.
        self.api_github = aiohttp.ClientSession()

    def get_unique_username(self, amount_to_gen):
        usernames = []
        for _ in range(amount_to_gen):
            letters_and_digits = string.ascii_letters + string.digits
            result_str = ''.join((random.choice(letters_and_digits) for i in range(self.length)))
            print(Fore.GREEN+"Generated --> ", result_str, Fore.RESET)
            usernames.append(result_str)
        return usernames

    async def check_username(self, username):
        try:
            send_data = await self.api_github.get(f"https://github.com/users/{username}")
            if send_data.status == 200:
                print(Fore.RED+f"[{username}] is taken")
            elif send_data.status == 404:
                print(Fore.GREEN+f"[{username}] is available")
        except:
            pass



def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

if __name__ == "__main__":
    _instance = Github()
    amount_to_gen = int(input(Fore.WHITE+"Enter amount to of usernames to generate and check: "))
    account = _instance.get_unique_username(amount_to_gen)
    for chunk in chunks(account, amount_to_gen):
        tries = asyncio.gather(*[_instance.check_username(username) for username in chunk])
        loop.run_until_complete(tries)
        asyncio.sleep(0.25)

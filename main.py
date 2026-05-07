# TELEGRAM : @lsahilxx
import requests, os, json, binascii, time, urllib3, base64, datetime, re, socket, ssl, asyncio, aiohttp, random, traceback
from protobuf_decoder.protobuf_decoder import Parser
from xDL import *
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from Pb2 import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2
import google.protobuf.json_format as json_format
# keep_alive removed: PORT CONFLICT with aiohttp web server (both used port 8080)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load emotes globally
def load_emotes_from_json():
    emotes_file = "emotes.json"
    try:
        if not os.path.exists(emotes_file): return {"numbers": {}, "names": {}}
        with open(emotes_file, 'r') as f:
            data = json.load(f)
        return {"numbers": data.get("EMOTES", {}).get("numbers", {}), "names": data.get("EMOTES", {}).get("names", {})}
    except: return {"numbers": {}, "names": {}}

def load_all_credentials():
    filename = "bot.txt"
    accounts = []
    try:
        if not os.path.exists(filename): return []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    data = json.loads(line)
                    for uid, password in data.items():
                        accounts.append((uid, password))
                except: continue
        return accounts
    except: return []

EMOTES_DATA = load_emotes_from_json()
NUMBER_EMOTES = EMOTES_DATA["numbers"]
NAME_EMOTES = EMOTES_DATA["names"]

def get_random_color(): return "[00FF00]" # Fallback color

# --- PROXY & DNS CONFIGURATION ---
def get_random_proxy():
    proxy_host = "change4.owlproxy.com"
    proxy_port = "7778"
    proxy_pass = "2933445"
    # Regenerate a fresh 8-digit SID to bypass blocks
    random_sid = random.randint(10000000, 99999999)
    proxy_user = f"hr6ckDl06980_custom_zone_BR_st__city_sid_{random_sid}_time_5"
    return f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

def get_connector():
    # Improved connector with custom DNS resolver (1.1.1.1) to fix [getaddrinfo failed]
    try:
        from aiohttp.resolver import AsyncResolver
        resolver = AsyncResolver(nameservers=["1.1.1.1", "1.0.0.1", "8.8.8.8", "8.8.4.4"])
        return aiohttp.TCPConnector(resolver=resolver, ssl=False, family=socket.AF_INET)
    except:
        # Fallback if AsyncResolver fails
        return aiohttp.TCPConnector(ssl=False)

# --- GLOBAL CONFIG ---
LEVEL_UP = "NIKI BOT"
start_spam_duration = 18
wait_after_match = 5
start_spam_delay = 0.1
region = 'IN'
ACTIVE_BOTS = []
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "NIKI-BOT-2026")

async def self_pinger():
    # Keep Render instance awake by pinging itself every 5 minutes
    url = "https://ffbots-1.onrender.com/"  # আপনার Render URL এখানে fixed
    await asyncio.sleep(30) # Initial wait for server to start
    while True:
        try:
            # Create a fresh session each time to avoid stale connections
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as resp:
                    print(f"✅ Self-ping OK: {resp.status}")
        except Exception as e:
            print(f"⚠️ Self-ping failed (harmless): {e}")
        await asyncio.sleep(300) # Ping every 5 minutes (more reliable than 10)

async def get_free_bot(task_id=None, timeout=15, reject_if_busy=False):
    for _ in range(timeout * 2):
        if task_id:
            already_handling = any(
                b.get('is_busy', False) and b.get('current_task_id') == task_id
                for b in ACTIVE_BOTS
            )
            if already_handling:
                if reject_if_busy:
                    return None
                await asyncio.sleep(0.5)
                continue
                
        bots = list(ACTIVE_BOTS)
        import random
        random.shuffle(bots)
        for bot in bots:
            if not bot.get('is_busy', False) and not bot.get('is_level_up', False) and bot.get('state', {}).get('online_writer') is not None:
                bot['is_busy'] = True
                if task_id:
                    bot['current_task_id'] = task_id
                return bot
        await asyncio.sleep(0.5)
    return None

def check_auth(request):
    auth_header = request.headers.get('Authorization')
    # Using simple Bearer token for API authentication
    if not auth_header or auth_header != f"Bearer {ADMIN_PASS}":
        return False
    return True

async def AuToUpDaTE():
    while True:
        try:
            proxy = get_random_proxy()
            from google_play_scraper import app
            # Scraping Play Store through proxy
            result = app('com.dts.freefireth', lang="fr", country='fr')
            version = result['version']
            return "https://loginbp.ggblueshark.com/", "OB53", version
        except Exception as e:
            print(f"Update Check Retry (Proxy: {e})")
            await asyncio.sleep(2)

async def GeNeRaTeAccEss(uid, password):
    while True:
        try:
            proxy = get_random_proxy()
            url = "https://100067.connect.garena.com/oauth/guest/token/grant"
            headers = {"Host": "100067.connect.garena.com", "User-Agent": await Ua(), "Content-Type": "application/x-www-form-urlencoded", "Connection": "close"}
            # Bug Fix: renamed 'data' to 'req_data' to avoid variable shadowing with response json
            req_data = {"uid": uid, "password": password, "response_type": "token", "client_type": "2", "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3", "client_id": "100067"}
            # Bug Fix: use ClientTimeout object instead of raw integer
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(connector=get_connector()) as session:
                async with session.post(url, headers=headers, data=req_data, proxy=proxy, timeout=timeout) as response:
                    if response.status == 200:
                        resp_json = await response.json()
                        return resp_json.get("open_id"), resp_json.get("access_token")
                    print(f"Access Failed ({response.status}), retrying...")
        except Exception as e:
            print(f"Proxy Access Error: {e}. Retrying with new SID...")
        await asyncio.sleep(2)

async def encrypted_proto(encoded_hex):
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    key = b'Yg&tc%DEuh6%Zc^8'; iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(encoded_hex, AES.block_size))

async def EncRypTMajoRLoGin(open_id, access_token, version):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"; major_login.platform_id = 1; major_login.client_version = version
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"; major_login.telecom_operator = "Verizon"; major_login.network_type = "WIFI"
    major_login.screen_width = 1920; major_login.screen_height = 1080; major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"; major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"; major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"; major_login.language = "en"; major_login.open_id = open_id
    major_login.open_id_type = "4"; major_login.device_type = "Handheld"
    major_login.access_token = access_token; major_login.platform_sdk_id = 1; major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"; major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235; major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519; major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010; major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992; major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3; major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1; major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3; major_login.cpu_type = 2; major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"; major_login.graphics_api = "OpenGLES2"; major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4; major_login.loading_time = 13564; major_login.release_channel = "android"
    major_login.android_engine_init_flag = 110009; major_login.if_push = 1; major_login.is_vpn = 1
    major_login.origin_platform_type = "4"; major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return await encrypted_proto(string)

async def MajorLogin(url, payload, Hr):
    while True:
        try:
            proxy = get_random_proxy()
            timeout = aiohttp.ClientTimeout(total=15)  # Bug Fix: use ClientTimeout object
            async with aiohttp.ClientSession(connector=get_connector()) as session:
                async with session.post(f"{url}MajorLogin", data=payload, headers=Hr, proxy=proxy, timeout=timeout) as response:
                    if response.status == 200: return await response.read()
                    print(f"MajorLogin Status: {response.status}, retrying...")
        except Exception as e:
            print(f"Retrying MajorLogin via Proxy... {e}")
        await asyncio.sleep(2)

async def GetLoginData(base_url, payload, token, Hr):
    while True:
        try:
            proxy = get_random_proxy()
            url = f"{base_url}/GetLoginData"
            Hr['Authorization'] = f"Bearer {token}"
            timeout = aiohttp.ClientTimeout(total=15)  # Bug Fix: use ClientTimeout object
            async with aiohttp.ClientSession(connector=get_connector()) as session:
                async with session.post(url, data=payload, headers=Hr, proxy=proxy, timeout=timeout) as response:
                    if response.status == 200: return await response.read()
                    print(f"GetLoginData Status: {response.status}, retrying...")
        except Exception as e:
            print(f"Retrying GetLoginData via Proxy... {e}")
        await asyncio.sleep(2)

async def SEndPacKeT(bot_state, TypE, PacKeT):
    # Wait for connection if it's temporarily down (up to 8 seconds)
    for _ in range(40):
        writer = bot_state.get('whisper_writer' if TypE == 'ChaT' else 'online_writer')
        if writer and not writer.is_closing():
            try:
                writer.write(PacKeT)
                await writer.drain()
                return
            except Exception:
                # Mark writer as dead so TCP handler reconnects
                key = 'whisper_writer' if TypE == 'ChaT' else 'online_writer'
                bot_state[key] = None
        await asyncio.sleep(0.2)
    raise Exception(f"❌ Error: {TypE} server disconnected after 8s wait")

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]; uid_length = len(uid_hex); encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex(); encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    headers = '0' * (16 - uid_length)  # Bug Fix: dynamic calculation, handles all UID lengths correctly
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

# --- BOT COMMANDS ---
async def join_teamcode_packet(team_code, key, iv, region):
    fields = {1: 4, 2: {4: bytes.fromhex("01090a0b121920"), 5: str(team_code), 6: 6, 8: 1, 9: {2: 800, 6: 11, 8: "1.111.1", 9: 5, 10: 1}}}
    packet_type = '0514' if region.lower() == "ind" else "0519" if region.lower() == "bd" else "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def start_auto_packet(key, iv, region):
    fields = {1: 9, 2: {1: 12480598706}}
    packet_type = '0514' if region.lower() == "ind" else "0519" if region.lower() == "bd" else "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def leave_squad_packet(key, iv, region):
    fields = {1: 7, 2: {1: 12480598706}}
    packet_type = '0514' if region.lower() == "ind" else "0519" if region.lower() == "bd" else "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def auto_start_loop(team_code, uid, chat_id, chat_type, key, iv, region, state, bot_state):
    bot_info = bot_state.get('bot_info')
    if bot_info: bot_info['is_busy'] = True
    try:
        while not state['stop_auto']:
            try:
                join_pkt = await join_teamcode_packet(team_code, key, iv, region)
                await SEndPacKeT(bot_state, 'OnLine', join_pkt)
                await asyncio.sleep(2)
                start_pkt = await start_auto_packet(key, iv, region)
                end_time = time.time() + start_spam_duration
                while time.time() < end_time and not state['stop_auto']:
                    await SEndPacKeT(bot_state, 'OnLine', start_pkt)
                    await asyncio.sleep(start_spam_delay)
                if state['stop_auto']: break
                await asyncio.sleep(wait_after_match)
                if state['stop_auto']: break
                leave_pkt = await leave_squad_packet(key, iv, region)
                await SEndPacKeT(bot_state, 'OnLine', leave_pkt)
                await asyncio.sleep(2)
            except Exception as e:
                print(f"❌ auto_start_loop error: {e}")
                traceback.print_exc()
                break
    finally:
        if bot_info: bot_info['is_busy'] = False
        state['running'] = False; state['stop_auto'] = False

async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, region, bot_state, max_retries=3):
    for _ in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv, region)
            await SEndPacKeT(bot_state, 'ChaT', P)
            return True
        except: await asyncio.sleep(0.5)
    return False

# --- TCP HANDLERS ---
async def TcPOnLine(ip, port, auth_token, bot_state, reconnect_delay=1.0):
    while True:
        writer = None
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, int(port)), timeout=20
            )
            bot_state['online_writer'] = writer
            writer.write(bytes.fromhex(auth_token))
            await writer.drain()
            print(f"✅ OnLine TCP connected to {ip}:{port}")
            # Keep reading to detect disconnect
            while True:
                try:
                    data = await asyncio.wait_for(reader.read(9999), timeout=60)
                    if not data:
                        print(f"⚠️ OnLine TCP: server closed connection. Reconnecting...")
                        break
                except asyncio.TimeoutError:
                    # Send a keepalive heartbeat every 60s to prevent idle timeout
                    if writer and not writer.is_closing():
                        try:
                            writer.write(b'')
                            await writer.drain()
                        except:
                            break
                    continue
        except Exception as e:
            print(f"🔴 OnLine TCP error: {e}. Reconnecting in {reconnect_delay}s...")
        finally:
            bot_state['online_writer'] = None
            if writer:
                try: writer.close(); await writer.wait_closed()
                except: pass
        await asyncio.sleep(reconnect_delay)

async def TcPChaT(ip, port, auth_token, key, iv, ready_event, region, bot_state, reconnect_delay=1.0):
    auto_start_state = {'running': False, 'stop_auto': False, 'task': None}
    
    while True:
        writer = None
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, int(port)), timeout=20
            )
            bot_state['whisper_writer'] = writer
            writer.write(bytes.fromhex(auth_token))
            await writer.drain()
            ready_event.set()
            print(f"✅ ChaT TCP connected to {ip}:{port}")
            while True:
                try:
                    data = await asyncio.wait_for(reader.read(9999), timeout=90)
                except asyncio.TimeoutError:
                    # 90 সেকেন্ড কোনো data নেই — keepalive পাঠাই
                    if writer and not writer.is_closing():
                        try:
                            writer.write(b'')
                            await writer.drain()
                            print("💓 ChaT heartbeat sent")
                        except:
                            print("⚠️ ChaT heartbeat failed, reconnecting...")
                            break
                    continue
                if not data:
                    print("⚠️ ChaT TCP: server closed. Reconnecting...")
                    break
                if data.hex().startswith("120000"):
                    try:
                        proto = DEcwHisPErMsG_pb2.DecodeWhisper()
                        proto.ParseFromString(bytes.fromhex(data.hex()[10:]))
                        uid = proto.Data.uid; chat_id = proto.Data.Chat_ID; inPuTMsG = proto.Data.msg.strip().lower()
                        print(f"Msg: {inPuTMsG} from {uid}")
                        
                        if inPuTMsG.startswith('/me'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                await safe_send_message(proto.Data.chat_type, "[B][C][FF0000]❌ Usage: /me [TeamCode] [Emote/Num] or [TeamCode] [UID] [Emote/Num]", uid, chat_id, key, iv, region, bot_state)
                                continue
                            
                            try:
                                team_code = parts[1]
                                last_part = parts[-1].lower()
                                emote_id = (NUMBER_EMOTES.get(last_part) or NAME_EMOTES.get(last_part))
                                # Bug Fix: safe UID parsing — if parts[2] is not a number (e.g. emote name), show proper error
                                if len(parts) == 4:
                                    try:
                                        target_uid = int(parts[2])
                                    except ValueError:
                                        await safe_send_message(proto.Data.chat_type, "[B][C][FF0000]❌ Usage: /me [Code] [UID] [Emote]", uid, chat_id, key, iv, region, bot_state)
                                        continue
                                else:
                                    target_uid = int(uid)
                                
                                if not emote_id:
                                    await safe_send_message(proto.Data.chat_type, f"[B][C][FF0000]❌ Invalid emote: {last_part}", uid, chat_id, key, iv, region, bot_state)
                                    continue
                                
                                bot_info = bot_state.get('bot_info')
                                if bot_info: bot_info['is_busy'] = True
                                try:
                                    initial_leave = await leave_squad_packet(key, iv, region)
                                    await SEndPacKeT(bot_state, 'OnLine', initial_leave)
                                    await asyncio.sleep(0.05)
    
                                    join_pkt = await GenJoinSquadsPacket(team_code, key, iv)
                                    await SEndPacKeT(bot_state, 'OnLine', join_pkt)
                                    await asyncio.sleep(0.2)
                                    
                                    emote_pkt = await Emote_k(target_uid, int(emote_id), key, iv, region)
                                    await SEndPacKeT(bot_state, 'OnLine', emote_pkt)
                                    await SEndPacKeT(bot_state, 'OnLine', emote_pkt)
                                    await SEndPacKeT(bot_state, 'OnLine', emote_pkt)
                                    await SEndPacKeT(bot_state, 'OnLine', emote_pkt)
                                    await asyncio.sleep(0.2)
                                    
                                    final_leave = await leave_squad_packet(key, iv, region)
                                    await SEndPacKeT(bot_state, 'OnLine', final_leave)
                                    await SEndPacKeT(bot_state, 'OnLine', final_leave)
                                    await SEndPacKeT(bot_state, 'OnLine', final_leave)
                                    
                                    await safe_send_message(proto.Data.chat_type, f"[B][C][00FF00]✅ Done! Joined {team_code} and sent emote.", uid, chat_id, key, iv, region, bot_state)
                                finally:
                                    if bot_info: bot_info['is_busy'] = False
                            except Exception as e:
                                print(f"❌ /me command error: {e}")
                                traceback.print_exc()
                                await safe_send_message(proto.Data.chat_type, "[B][C][FF0000]❌ Execution Error!", uid, chat_id, key, iv, region, bot_state)

                        elif inPuTMsG.startswith('/e'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) == 1 or (len(parts) == 2 and parts[1].lower() == 'list'):
                                msg = f"[B][C][00FF00]🎭 EMOTE SYSTEM\n• Numbers: 1-{len(NUMBER_EMOTES)}\n• Names: {len(NAME_EMOTES)} names\nUsage:\n/e [name/num]\n/e [uid] [name/num]"
                                await safe_send_message(proto.Data.chat_type, msg, uid, chat_id, key, iv, region, bot_state)
                                continue
                            
                            try:
                                last_part = parts[-1].lower()
                                # Bug Fix: detect direct emote ID by checking if it's a large number (>900000)
                                # Old logic required startswith("9090") which was too restrictive
                                is_direct = last_part.isdigit() and int(last_part) > 900000
                                emote_id = int(last_part) if is_direct else (NUMBER_EMOTES.get(last_part) or NAME_EMOTES.get(last_part))
                                
                                if not emote_id:
                                    await safe_send_message(proto.Data.chat_type, f"[B][C][FF0000]❌ Invalid emote: {last_part}", uid, chat_id, key, iv, region, bot_state)
                                    continue
                                
                                target_uids = [int(parts[1])] if len(parts) == 3 else [int(uid)]
                                bot_info = bot_state.get('bot_info')
                                if bot_info: bot_info['is_busy'] = True
                                try:
                                    for t_uid in target_uids:
                                        pkt = await Emote_k(t_uid, int(emote_id), key, iv, region)
                                        await SEndPacKeT(bot_state, 'OnLine', pkt)
                                        await asyncio.sleep(0.1)
                                    await safe_send_message(proto.Data.chat_type, f"[B][C][00FF00]✅ Emote Sent!", uid, chat_id, key, iv, region, bot_state)
                                finally:
                                    if bot_info: bot_info['is_busy'] = False
                            except Exception as e:
                                print(f"❌ /e command error: {e}")
                                await safe_send_message(proto.Data.chat_type, "[B][C][FF0000]❌ Format Error!", uid, chat_id, key, iv, region, bot_state)

                        elif inPuTMsG in ('/3', '/4', '/5', '/6'):
                            limit = int(inPuTMsG[1:])
                            initial_message = f"[B][C][00FFFF]\n\nCreating {limit}-Player Group...\n\n"
                            await safe_send_message(proto.Data.chat_type, initial_message, uid, chat_id, key, iv, region, bot_state)
                            
                            try:
                                bot_info = bot_state.get('bot_info')
                                if bot_info: bot_info['is_busy'] = True
                                try:
                                    PAc = await OpEnSq(key, iv, region)
                                    await SEndPacKeT(bot_state, 'OnLine', PAc)
                                    await asyncio.sleep(1.0)
                                    
                                    C = await cHSq(limit, uid, key, iv, region)
                                    await SEndPacKeT(bot_state, 'OnLine', C)
                                    await asyncio.sleep(1.0)
                                    
                                    V = await SEnd_InV(limit, uid, key, iv, region)
                                    await SEndPacKeT(bot_state, 'OnLine', V)
                                    await asyncio.sleep(1.0)
                                    await SEndPacKeT(bot_state, 'OnLine', V)
                                    
                                    async def inline_leave():
                                        try:
                                            await asyncio.sleep(8.0)
                                            E = await leave_squad_packet(key, iv, region)
                                            await SEndPacKeT(bot_state, 'OnLine', E)
                                        finally:
                                            if bot_info: bot_info['is_busy'] = False
                                    
                                    asyncio.create_task(inline_leave())
                                    
                                    success_message = f"[B][C][00FF00]✅ SUCCESS! {limit}-Player Group invitation sent to {uid}!\n"
                                    await safe_send_message(proto.Data.chat_type, success_message, uid, chat_id, key, iv, region, bot_state)
                                except Exception as e:
                                    if bot_info: bot_info['is_busy'] = False
                                    raise e
                            except Exception as e:
                                await safe_send_message(proto.Data.chat_type, f"[B][C][FF0000]❌ ERROR: {str(e)}", uid, chat_id, key, iv, region, bot_state)

                        elif inPuTMsG.startswith('/lw '):
                            team_code = inPuTMsG.split()[1]
                            if auto_start_state['running']: continue
                            auto_start_state['stop_auto'] = False; auto_start_state['running'] = True
                            await safe_send_message(proto.Data.chat_type, f"[B][C][00FF00]Auto started for {team_code}", uid, chat_id, key, iv, region, bot_state)
                            auto_start_state['task'] = asyncio.create_task(auto_start_loop(team_code, uid, chat_id, proto.Data.chat_type, key, iv, region, auto_start_state, bot_state))
                        elif inPuTMsG == '/stop_auto':
                            auto_start_state['stop_auto'] = True; auto_start_state['running'] = False
                            if auto_start_state['task']: auto_start_state['task'].cancel()
                            await safe_send_message(proto.Data.chat_type, "[B][C][00FF00]Stopped", uid, chat_id, key, iv, region, bot_state)
                        elif inPuTMsG in ('/help', 'help', '/menu'):
                            help_msg = (
                                f"[B][C][00FFFF]🌟 NIKI BOT - COMMAND MENU 🌟\n"
                                f"[FFFFFF]────────────────────\n"
                                f"[00FF00]🎮 MATCH BOT:\n"
                                f"• /lw [Code] -> Auto Start Match\n"
                                f"• /stop_auto -> Stop Match Bot\n\n"
                                f"[FFFF00]👥 GROUP COMMANDS:\n"
                                f"• /3, /4, /5, /6 -> Set Group Limit\n"
                                f"• /exit -> Leave Group\n\n"
                                f"[FF00FF]🎭 EMOTE COMMANDS:\n"
                                f"• /e [name] -> Send Emote Self\n"
                                f"• /e [uid] [name] -> Send to UID\n"
                                f"• /me [Code] [name] -> Fast Attack\n\n"
                                f"[00FFFF]⚡ SYSTEM:\n"
                                f"• /e list -> View All Emotes\n"
                                f"[FFFFFF]────────────────────\n"
                                f"[00FF00]Developed by NIKI BOT 👑"
                            )
                            await safe_send_message(proto.Data.chat_type, help_msg, uid, chat_id, key, iv, region, bot_state)
                    except: pass
        except Exception as e:
            print(f"🔴 ChaT TCP error: {e}. Reconnecting in {reconnect_delay}s...")
        finally:
            bot_state['whisper_writer'] = None
            ready_event.clear()  # Reset event so wait_for_bot waits for reconnect
            if writer:
                try: writer.close(); await writer.wait_closed()
                except: pass
        await asyncio.sleep(reconnect_delay)

async def run_bot_instance(uid, password):
    print(f"🚀 Starting Bot Instance: {uid}")
    while True:  # OUTER loop: Always reconnect, never give up
        bot_info = None
        chat_task = None
        online_task = None
        watchdog_task = None
        try:
            # --- Step 1: Get Garena OAuth Token ---
            open_id, access_token = await GeNeRaTeAccEss(uid, password)
            if not open_id:
                print(f"❌ Login Failed for {uid}, retrying in 10s...")
                await asyncio.sleep(10)
                continue
            
            # --- Step 2: Get Game Version & Login ---
            login_url, ob, version = await AuToUpDaTE()
            Hr = {'User-Agent': Uaa(), 'Connection': "Keep-Alive", 'Accept-Encoding': "gzip",
                  'Content-Type': "application/x-www-form-urlencoded", 'X-Unity-Version': "2018.4.11f1",
                  'X-GA': "v1 1", 'ReleaseVersion': ob}
            payload = await EncRypTMajoRLoGin(open_id, access_token, version)
            
            login_resp = await MajorLogin(login_url, payload, Hr)
            if not login_resp:
                print(f"❌ MajorLogin Failed for {uid}, retrying in 5s...")
                await asyncio.sleep(5)
                continue
            
            auth = MajoRLoGinrEs_pb2.MajorLoginRes()
            auth.ParseFromString(login_resp)
            
            login_data_resp = await GetLoginData(auth.url, payload, auth.token, Hr)
            if not login_data_resp:
                print(f"❌ LoginData Failed for {uid}, retrying in 5s...")
                await asyncio.sleep(5)
                continue
            
            # --- Step 3: Extract IPs and Connect ---
            ports = PorTs_pb2.GetLoginData()
            ports.ParseFromString(login_data_resp)
            chat_ip, chat_port = ports.AccountIP_Port.split(":")
            online_ip, online_port = ports.Online_IP_Port.split(":")
            auth_token = await xAuThSTarTuP(
                int(auth.account_uid), auth.token,
                int(auth.timestamp), auth.key, auth.iv
            )
            
            # --- Step 4: Start TCP connections ---
            ready = asyncio.Event()
            bot_state = {'online_writer': None, 'whisper_writer': None}
            bot_region = getattr(auth, 'region', 'IND')
            bot_info = {'uid': uid, 'key': auth.key, 'iv': auth.iv, 'region': bot_region, 'state': bot_state, 'is_busy': False}
            bot_state['bot_info'] = bot_info
            ACTIVE_BOTS.append(bot_info)
            print(f"✅ Bot {uid} ({bot_region}) is now Online!")

            # --- Step 5: Watchdog — যদি দুটো connection-ই 45s ধরে dead থাকে → full re-login ---
            async def session_watchdog(b_state, b_uid):
                # প্রথম 60s দাও connection establish হওয়ার জন্য
                await asyncio.sleep(60)
                consecutive_dead = 0
                while True:
                    await asyncio.sleep(15)
                    online_alive = b_state.get('online_writer') is not None
                    chat_alive = b_state.get('whisper_writer') is not None
                    if not online_alive and not chat_alive:
                        consecutive_dead += 1
                        print(f"⚠️ Watchdog [{b_uid}]: Both connections dead ({consecutive_dead * 15}s)...")
                        if consecutive_dead >= 3:  # 45 সেকেন্ড dead → full re-login
                            print(f"🔄 Watchdog [{b_uid}]: Session expired! Forcing full re-login...")
                            return  # watchdog বের হলে gather শেষ হবে → re-login হবে
                    else:
                        if consecutive_dead > 0:
                            print(f"✅ Watchdog [{b_uid}]: Connection restored!")
                        consecutive_dead = 0  # কোনো একটা alive থাকলে reset

            chat_task = asyncio.create_task(TcPChaT(chat_ip, chat_port, auth_token, auth.key, auth.iv, ready, bot_region, bot_state))
            online_task = asyncio.create_task(TcPOnLine(online_ip, online_port, auth_token, bot_state))
            watchdog_task = asyncio.create_task(session_watchdog(bot_state, uid))

            # Watchdog শেষ হলে (session dead) → TCP tasks বন্ধ করো → re-login হবে
            await watchdog_task

            print(f"🔄 Bot {uid}: Watchdog triggered re-login. Stopping old connections...")
            if chat_task and not chat_task.done(): chat_task.cancel()
            if online_task and not online_task.done(): online_task.cancel()
            # Cancel হওয়ার সময় দাও
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"🔥 Bot {uid} critical error: {e}")
            traceback.print_exc()
            if chat_task and not chat_task.done(): chat_task.cancel()
            if online_task and not online_task.done(): online_task.cancel()
            if watchdog_task and not watchdog_task.done(): watchdog_task.cancel()
        finally:
            # Always clean up from ACTIVE_BOTS before retry
            if bot_info and bot_info in ACTIVE_BOTS:
                ACTIVE_BOTS.remove(bot_info)
        
        print(f"🔄 Bot {uid} re-logging in 5s...")
        await asyncio.sleep(5)

from aiohttp import web

ACTIVE_GC_SESSIONS = {}

async def monitor_gc_session(team_code):
    while True:
        await asyncio.sleep(1.0)
        session = ACTIVE_GC_SESSIONS.get(team_code)
        if not session:
            break
        
        if time.time() - session['last_activity'] >= 10.0:
            bot = session['bot']
            try:
                final_leave = await leave_squad_packet(bot['key'], bot['iv'], bot['region'])
                for _ in range(3):
                    await SEndPacKeT(bot['state'], 'OnLine', final_leave)
            except:
                pass
            finally:
                bot['is_busy'] = False
                bot['current_task_id'] = None
                if team_code in ACTIVE_GC_SESSIONS:
                    del ACTIVE_GC_SESSIONS[team_code]
            break

async def handle_ping(request):
    return web.Response(text="Bot is alive!")

async def handle_emote(request):
    if not check_auth(request):
        return web.json_response({"error": "Unauthorized Access"}, status=401)
    try:
        data = await request.json()
        team_code = data.get('team_code')
        emote_id = data.get('emote_id')
        target_uids = data.get('target_uids', [])
        uids_to_emote = target_uids if target_uids else []
        
        # Check if we already have a 10s active session for this team_code
        session = ACTIVE_GC_SESSIONS.get(team_code)
        
        if session:
            # 2. Re-use existing bot in this GC to prevent jamming
            bot = session['bot']
            session['last_activity'] = time.time()
            
            for uid in uids_to_emote:
                if not uid: continue
                try:
                    t_uid = int(uid)
                    emote_pkt = await Emote_k(t_uid, int(emote_id), bot['key'], bot['iv'], bot['region'])
                    for _ in range(2):
                        await SEndPacKeT(bot['state'], 'OnLine', emote_pkt)
                        await asyncio.sleep(0.1)
                    await asyncio.sleep(2.5)
                except: pass
                
            return web.json_response({"success": True, "message": f"Fast Emote sent using active bot {bot['uid']}"})

        else:
            # 1. New GC, get a new free bot
            bot = await get_free_bot(task_id=f"session_{team_code}", reject_if_busy=True)
            if not bot:
                return web.json_response({"error": "No free bots available right now!"}, status=400)
                
            try:
                # Cleanup any ghost squads
                initial_leave = await leave_squad_packet(bot['key'], bot['iv'], bot['region'])
                await SEndPacKeT(bot['state'], 'OnLine', initial_leave)
                await asyncio.sleep(0.05)
        
                # Join new GC
                join_pkt = await GenJoinSquadsPacket(team_code, bot['key'], bot['iv'])
                await SEndPacKeT(bot['state'], 'OnLine', join_pkt)
                await asyncio.sleep(0.2)
                
                # Send emotes
                for uid in uids_to_emote:
                    if not uid: continue
                    try:
                        t_uid = int(uid)
                        emote_pkt = await Emote_k(t_uid, int(emote_id), bot['key'], bot['iv'], bot['region'])
                        for _ in range(2):
                            await SEndPacKeT(bot['state'], 'OnLine', emote_pkt)
                            await asyncio.sleep(0.1)
                        await asyncio.sleep(2.5)
                    except: pass
                    
                # Create the 10s session instead of leaving
                ACTIVE_GC_SESSIONS[team_code] = {
                    'bot': bot,
                    'last_activity': time.time()
                }
                asyncio.create_task(monitor_gc_session(team_code))
                
            except Exception as e:
                bot['is_busy'] = False
                bot['current_task_id'] = None
                raise e

        return web.json_response({"success": True, "message": f"Emote sent to {len(uids_to_emote)} targets using bot {bot['uid']}"})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def handle_group_invite(request):
    if not check_auth(request):
        return web.json_response({"error": "Unauthorized Access"}, status=401)
    try:
        data = await request.json()
        limit = int(data.get('limit', 4))
        target_uid = data.get('target_uid')
        
        bot = await get_free_bot(task_id=f"invite_{target_uid}", reject_if_busy=True)
        if not bot:
            return web.json_response({"error": "Bot is already processing this target or no bots available!"}, status=400)
            
        try:
            t_uid = int(target_uid) if target_uid else int(bot['uid'])
            
            PAc = await OpEnSq(bot['key'], bot['iv'], bot['region'])
            await SEndPacKeT(bot['state'], 'OnLine', PAc)
            await asyncio.sleep(1.0)
            
            C = await cHSq(limit, t_uid, bot['key'], bot['iv'], bot['region'])
            await SEndPacKeT(bot['state'], 'OnLine', C)
            await asyncio.sleep(1.0)
            
            V = await SEnd_InV(limit, t_uid, bot['key'], bot['iv'], bot['region'])
            await SEndPacKeT(bot['state'], 'OnLine', V)
            await asyncio.sleep(1.0)
            await SEndPacKeT(bot['state'], 'OnLine', V)
            
            async def delayed_leave():
                try:
                    await asyncio.sleep(8.0)
                    E = await leave_squad_packet(bot['key'], bot['iv'], bot['region'])
                    await SEndPacKeT(bot['state'], 'OnLine', E)
                finally:
                    bot['is_busy'] = False
                    bot['current_task_id'] = None
            
            asyncio.create_task(delayed_leave())
            return web.json_response({"success": True, "message": f"Group invitation ({limit}) sent to {t_uid} using bot {bot['uid']}"})
        except Exception as e:
            bot['is_busy'] = False
            bot['current_task_id'] = None
            raise e
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

LEVEL_UP_TASKS = {}

async def handle_match_bot_stats(request):
    if not check_auth(request):
        return web.json_response({"error": "Unauthorized Access"}, status=401)
    
    bot_uid = request.query.get('bot_uid')
    if not bot_uid:
        return web.json_response({"running": False, "error": "bot_uid required"})
        
    task_info = LEVEL_UP_TASKS.get(bot_uid)
    if not task_info:
        return web.json_response({"running": False})
        
    runtime = 0
    if task_info['running'] and task_info['start_time']:
        runtime = int(time.time() - task_info['start_time'])
        
    return web.json_response({
        "running": task_info['running'],
        "games_played": task_info['games_played'],
        "runtime": runtime,
        "bot_uid": task_info['bot_uid'],
        "team_code": task_info['team_code']
    })

async def handle_verify_github_pass(request):
    if not check_auth(request):
        return web.json_response({"error": "Unauthorized Access"}, status=401)
    try:
        data = await request.json()
        input_pass = data.get('password')
        
        # Fetching password from the user's provided GitHub Gist
        GITHUB_URL = "https://gist.githubusercontent.com/rakibkumar151/ded10243095bc97e4c89e31e593112f9/raw/c919f226e7eeed8592d3ad83eeea6bcdf7bca508/pass.txt"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(GITHUB_URL) as response:
                if response.status == 200:
                    github_pass = (await response.text()).strip()
                    if input_pass == github_pass:
                        return web.json_response({"success": True})
                    else:
                        return web.json_response({"error": "Invalid Level-Up Password"}, status=401)
                else:
                    # Fallback if github is down or URL wrong
                    return web.json_response({"error": "Auth Server Down"}, status=500)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def handle_auto_start(request):
    if not check_auth(request):
        return web.json_response({"error": "Unauthorized Access"}, status=401)
    try:
        data = await request.json()
        action = data.get('action')
        team_code = data.get('team_code')
        bot_uid = data.get('bot_uid')
        
        if not bot_uid:
            return web.json_response({"error": "Bot UID required"}, status=400)
            
        if action == 'stop':
            task_info = LEVEL_UP_TASKS.get(bot_uid)
            if task_info:
                task_info['stop_auto'] = True
                task_info['running'] = False
                if task_info['task']:
                    task_info['task'].cancel()
                    
            for b in ACTIVE_BOTS:
                if str(b['uid']) == str(bot_uid):
                    b['is_level_up'] = False
                    b['is_busy'] = False
                    break
                    
            if bot_uid in LEVEL_UP_TASKS:
                del LEVEL_UP_TASKS[bot_uid]
                
            return web.json_response({"success": True, "message": "Auto start stopped"})
            
        if not team_code:
            return web.json_response({"error": "Team Code required"}, status=400)

        bot = None
        for b in ACTIVE_BOTS:
            if str(b['uid']) == str(bot_uid):
                bot = b
                break
                
        if not bot:
            return web.json_response({"error": "Bot not found or offline"}, status=400)
            
        if bot.get('is_level_up', False) or bot.get('is_busy', False):
            return web.json_response({"error": "Bot is currently busy or already doing Level Up"}, status=400)

        bot['is_level_up'] = True
        bot['is_busy'] = True
        
        task_info = {
            'running': True,
            'stop_auto': False,
            'task': None,
            'team_code': team_code,
            'games_played': 0,
            'start_time': time.time(),
            'bot_uid': bot_uid
        }
        LEVEL_UP_TASKS[bot_uid] = task_info
        
        async def web_auto_start_loop():
            try:
                while not task_info['stop_auto']:
                    bot['is_busy'] = True
                    try:
                        join_pkt = await join_teamcode_packet(team_code, bot['key'], bot['iv'], bot['region'])
                        await SEndPacKeT(bot['state'], 'OnLine', join_pkt)
                        await asyncio.sleep(2.5)
                        
                        if task_info['stop_auto']: break
                        
                        start_pkt = await start_auto_packet(bot['key'], bot['iv'], bot['region'])
                        for i in range(40): 
                            if task_info['stop_auto']: break
                            await SEndPacKeT(bot['state'], 'OnLine', start_pkt)
                            await asyncio.sleep(0.25)
                        
                        if task_info['stop_auto']: break
                        
                        task_info['games_played'] += 1
                        await asyncio.sleep(wait_after_match) 
                        
                        if task_info['stop_auto']: break
                        
                        leave_pkt = await leave_squad_packet(bot['key'], bot['iv'], bot['region'])
                        await SEndPacKeT(bot['state'], 'OnLine', leave_pkt)
                        await asyncio.sleep(2.5)
                    except Exception as e:
                        print(f"Error in web auto start round: {e}")
                        await asyncio.sleep(2.5)
            except Exception as e:
                print(f"Web Auto Start Critical Error: {e}")
            finally:
                bot['is_busy'] = False
                bot['is_level_up'] = False
                if bot_uid in LEVEL_UP_TASKS:
                    del LEVEL_UP_TASKS[bot_uid]

        task_info['task'] = asyncio.create_task(web_auto_start_loop())
        return web.json_response({"success": True, "message": f"Auto start initiated for {team_code} using Bot {bot_uid}"})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def handle_bots(request):
    if not check_auth(request):
        return web.json_response({"error": "Unauthorized Access"}, status=401)
    try:
        bots = [{"uid": b['uid'], "region": b['region'], "is_busy": b.get('is_busy', False), "is_level_up": b.get('is_level_up', False)} for b in ACTIVE_BOTS]
        return web.json_response({"bots": bots})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def handle_login(request):
    try:
        data = await request.json()
        user = data.get('username')
        pwd = data.get('password')
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            return web.json_response({"success": True, "token": ADMIN_PASS})
        else:
            return web.json_response({"error": "Invalid Username or Password"}, status=401)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def handle_options(request):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS, HEAD",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    }
    return web.Response(headers=headers)

@web.middleware
async def cors_middleware(request, handler):
    if request.method == 'OPTIONS':
        return await handle_options(request)
    
    try:
        response = await handler(request)
        response.headers.update({
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS, HEAD",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        })
        return response
    except web.HTTPException as ex:
        ex.headers.update({
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS, HEAD",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        })
        raise ex

async def start_web_server():
    app = web.Application(middlewares=[cors_middleware])
    app.router.add_get('/', handle_ping)
    app.router.add_post('/api/emote', handle_emote)
    app.router.add_post('/api/group_invite', handle_group_invite)
    app.router.add_post('/api/auto_start', handle_auto_start)
    app.router.add_get('/api/bots', handle_bots)
    app.router.add_post('/api/login', handle_login)
    app.router.add_get('/api/match_bot_stats', handle_match_bot_stats)
    app.router.add_post('/api/verify_github_pass', handle_verify_github_pass)
    
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌐 Web API Server started on port {port}")

async def MaiiiinE():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"--- {LEVEL_UP} MULTI-ID SYSTEM ---")
    
    # Start web server first (no port conflict since keep_alive removed)
    await start_web_server()
    
    # Start self-pinger in background
    asyncio.create_task(self_pinger())
    
    # Load accounts once
    accounts = load_all_credentials()
    if not accounts:
        print("❌ No accounts found in bot.txt! Cannot start.")
        # Keep the web server alive even if no accounts
        while True:
            await asyncio.sleep(60)
    
    print(f"📝 Loaded {len(accounts)} accounts. Starting bots...")
    
    # Each bot runs in its own infinite loop (never stops)
    while True:
        try:
            bot_tasks = [asyncio.create_task(run_bot_instance(uid, pwd)) for uid, pwd in accounts]
            await asyncio.gather(*bot_tasks, return_exceptions=True)
            print("⚠️ All bot tasks ended. Restarting in 5s...")
        except Exception as e:
            print(f"🔥 Critical Main Error: {e}. Auto-recovering in 5s...")
        await asyncio.sleep(5)

if __name__ == '__main__':
    try:
        asyncio.run(MaiiiinE())
    except KeyboardInterrupt:
        print("\nStopping bot...")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        traceback.print_exc()
        input("Press Enter to exit...") # Keeps the window open if it crashes

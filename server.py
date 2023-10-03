import socket
import threading
import binascii
import psycopg2
from twos_complement import twos_complement


SERVER = "YOUR_IP"
PORT = YOUR_PORT


db_url = "localhost"
db_port = 5432
db_name = "gumbaz_db"
db_username = "gumbaz_user"
db_password = "gumbaz_password"


def decodethis(data, imei):
    # Get the Codec Data
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_username,
        password=db_password,
        host=db_url,
        port=db_port
    )

    codec = int(data[16:18], 16)

    if codec == 8:
        drone_id = imei
        length = int(data[8:16], 16)
        record = int(data[18:20], 16)
        timestamp = int(data[20:36], 16)
        priority = int(data[36:38], 16)
        longitude = int(data[38:46], 16)
                latitude = int(data[46:54], 16)
        altitude = int(data[54:58], 16)
        angle = int(data[58:62], 16)
        satellites = int(data[62:64], 16)
        speed = int(data[64:68], 16)

        # Convert the Integer Location to Longitude and Latitude format
        longitude = loc_convert(longitude)
        latitude = loc_convert(latitude)

        print("IMEI: " + drone_id)  # Вывести IMEI
        print("Length: " + str(length))
        print("Record: " + str(record))
        print("Timestamp: " + str(timestamp))
        print("Priority: " + str(priority))
        print("Latitude: " + str(latitude))
        print("Longitude: " + str(longitude))
        print("Altitude: " + str(altitude))
        print("Angle: " + str(angle))
                print("Satellites: " + str(satellites))
        print("Speed: " + str(speed))
        print("")

        data_to_insert = [
            length, record, timestamp, priority, longitude, latitude, altitude, angle, satellites, $
        ]

        # Проверка на наличие символов NUL в data_to_insert
        for i, value in enumerate(data_to_insert):
            if '\x00' in str(value):
                # Обработка символа NUL, например, заменой его на пустую строку
                data_to_insert[i] = str(value).replace('\x00', '')

        cur = conn.cursor()
        sql = "INSERT INTO tracker_data(length, record, timestamp, priority, longitude, latitude, a$
        cur.execute(sql, data_to_insert)
        conn.commit()
        conn.close()

        
        # Необходимо отправить данные записи обратно в виде 4 байтов
        return record.to_bytes(4, 'big')



    ### Location converter
def loc_convert(loc):
    check = 2 ** 31
    if (loc < check):
        loc_int = float(loc) / 10 ** 7
        return loc_int

    elif (loc > check):
        loc_bin = bin(loc).replace("0b", "")
        loc_bin = twos_complement(loc_bin)
        loc_int = float(int(loc_bin, 2)) / 10 ** 7
        return loc_int * -1

    elif (loc == 0):
        return "0"
### Handle the Client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    imei_data = conn.recv(1280)
    imei = imei_data.decode('utf-8', errors='ignore')
    print("IMEI: " + imei)
    message = '\x01'
    message = message.encode('utf-8')
    conn.send(message)

    while connected:
        try:
            data = conn.recv(1280)
            received = binascii.hexlify(data)
            record = decodethis(received, imei)
            conn.send(record)
        
        except socket.error:
            print("Error Occurred.")
            break
    conn.close()


### Start the server
def start():
    s.listen()
    print("Server is listening ...")

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

## Main
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER, PORT))
print("[STARTING] server is starting...")
start()




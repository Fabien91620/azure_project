from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.storage.blob.blockblobservice import BlockBlobService
from msrest.authentication import CognitiveServicesCredentials
from mysql import connector
from PIL import Image
import streamlit as st
import io

import credentials

container_name = 'images'
local_image_path = "tmp/imgTmp.png"


def get_computer_vision():
    computervision_client = ComputerVisionClient(credentials.COG_ENDPOINT,
                                                 CognitiveServicesCredentials(credentials.COG_KEY))
    return computervision_client


def get_connection_azure():
    account_name = 'sa0azure0project'
    account_key = 'JTkJWy/QOGVD22xD2RKvgsxYFNhBRBFQkp594Dz5DC0IIquhzTdTxz3D9pxGn2dSm359bMClksF1+AStqM8uPQ=='
    block_blob_service = BlockBlobService(
        account_name=account_name,
        account_key=account_key
    )
    return block_blob_service


def connect_db():
    engine = connector.connect(host='db-azure-project.mysql.database.azure.com',
                               database='azure_project',
                               user='iabdroot',
                               password='abcdef1&')

    return engine


def add_image_in_azure(blob_name, blob):
    azure = get_connection_azure()
    # azure.create_blob_from_path(container_name=container_name,blob_name=blob_name,file_path=path)
    azure.create_blob_from_bytes(container_name=container_name, blob_name=blob_name, blob=blob)
    url = f"https://sa0azure0project.blob.core.windows.net/{container_name}/{blob_name}"
    return url


def load_image(image_file):
    img = Image.open(image_file)
    print(type(img))
    return img


def pil_to_bytes(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    image.save(local_image_path, format="png")
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def add_path_to_db(path, tags=None):
    if tags is None:
        tags = []
    insert = f"insert into image (url) values ('{path}')"

    cursor = connection.cursor(dictionary=True, buffered=True)
    cursor.execute(insert)
    connection.commit()

    for tag in tags:
        select = f"select idtag from tag where name = '{tag}'"
        cursor.execute(select)
        resultset = cursor.fetchall()
        idtag = ""
        if len(resultset) != 0:
            idtag = resultset[0]["idtag"]
        else:
            query = f"SELECT idtag FROM tag where name = '{tag}'"
            cursor.execute(query)
            if cursor.rowcount > 0:
                idtag = cursor.fetchone()["idtag"]
            else:
                query = f"insert into tag (name) values ('{tag}')"
                cursor.execute(query)
                connection.commit()
                select = f"select idtag from tag where name = '{tag}'"
                cursor.execute(select)
                idtag = cursor.fetchone()["idtag"]

        query_join_table = "insert into tag_image (idimage, idtag_image) " \
                           f"values ( (select max(idimage) from image), {idtag} )"
        cursor.execute(query_join_table)
        connection.commit()

    # resultat = cursor.fetchall()
    # return json.dumps(resultat)


def get_azure_tags():
    query = "select name from tag"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)

    tag_res = []
    resultat = cursor.fetchall()
    print(resultat)
    for result in resultat:
        if result["name"] not in tag_res:
            tag_res.append(result["name"])

    return tag_res


def display_filtered_images(selection):
    select = f"select * from azure_project.image i inner join azure_project.tag_image ti on i.idimage = ti.idimage inner join azure_project.tag t on t.idtag = ti.idtag_image where t.name = '{selection}'"
    cursor = connection.cursor(dictionary=True, buffered=True)
    cursor.execute(select)

    for row in cursor.fetchall():
        st.image(row["url"], caption=f'{selection}')


connection = connect_db()
connection2 = get_connection_azure()
selection = st.selectbox("Filtrer un tag", get_azure_tags())
image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])
if image_file is not None:
    file_details = {"filename": image_file.name, "filetype": image_file.type,
                    "filesize": image_file.size}
    st.write(file_details)

    st.image(load_image(image_file), width=250)

    img = load_image(image_file)
    print("image chargee")
    get_azure_tags()
    img = pil_to_bytes(img)
    ia = get_computer_vision()
    img_stream = open(local_image_path, "rb")
    description = ia.describe_image_in_stream(img_stream)
    print(description)
    file_path = add_image_in_azure(image_file.name, img)
    print(file_path)
    add_path_to_db(file_path, description.tags)
if selection is not None:
    print("your selection ", selection)
    display_filtered_images(selection)

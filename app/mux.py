import os
from dotenv import load_dotenv
import mux_python
import requests
from fastapi import UploadFile

load_dotenv()

# env setup
configuration = mux_python.Configuration()
configuration.username = os.environ["MUX_ACCESS_TOKEN_ID"]
configuration.password = os.environ["MUX_SECRET_KEY"]

# api clients
assets_api = mux_python.AssetsApi(mux_python.ApiClient(configuration))
uploads_api = mux_python.DirectUploadsApi(mux_python.ApiClient(configuration))


def upload_to_mux(file: UploadFile) -> str:
    try:
        # policy should change to 'drm' when I have access to that
        playback_policies = [mux_python.PlaybackPolicy.PUBLIC]

        # get temp url to upload to
        new_asset_settings = mux_python.CreateAssetRequest(playback_policy=playback_policies)
        create_upload = mux_python.CreateUploadRequest(new_asset_settings=new_asset_settings)
        upload_response = uploads_api.create_direct_upload(create_upload)
        upload_url = upload_response.data.url

        # use the created url to upload the file
        response = requests.put(upload_url, data=file.file)
        if response.status_code != 200:
            raise Exception(f"Upload failed: {response.text}")

        upload_id = upload_response.data.id
        upload_status = uploads_api.get_direct_upload(upload_id)

        if upload_status.data.asset_id:
            return upload_status.data.asset_id
        raise RuntimeError("Internal Server error while uploading. Response data: ", upload_status.data)

    except mux_python.ApiException as e:
        raise RuntimeError(f"API error: {e.body}")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise RuntimeError(f"Upload error: {str(e)}")


def get_asset_details(asset_id: str) -> dict:
    try:
        asset = assets_api.get_asset(asset_id)
        if asset.data.status == 'ready':
            playback_id = next((p.id for p in asset.data.playback_ids if p.policy == "public"), None)
            if not playback_id:
                raise Exception("No playback ID found")
            return {"asset_id": asset.data.id, "status": asset.data.status, "playback_ids": [p.id for p in asset.data.playback_ids]}
    except mux_python.ApiException as e:
        raise RuntimeError(f"API error: {e.body}")
    except Exception as e:
        print(f"An error occurred: {e}")


def delete_asset(asset_id: str) -> None:
    try:
        assets_api.delete_asset(asset_id)
    except mux_python.ApiException as e:
        raise RuntimeError(f"API error: {e.body}")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise RuntimeError(f"Delete error: {str(e)}")

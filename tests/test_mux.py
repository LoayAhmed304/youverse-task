from app.mux import upload_to_mux, get_asset_details

file_path = "C:\\Users\\Loay\\Videos\\mux.mp4"

try:
    # test uploading and receiving the asset id (will be inserted in db)
    result: str = upload_to_mux(file_path)
    print("Upload Successfull!")
    print("Asset: ", result)
    assert result is not None and result != ""

    # test getting the playback from asset id
    print("\n\nGetting asset details test")
    asset_details = get_asset_details(result)
    assert asset_details is not None and asset_details["status"] == "ready"
    print("Asset details retrieved!")
    print("Asset ID:", asset_details["asset_id"])
    print("Asset status:", asset_details["status"])
    print("Playback ID:", asset_details["playback_ids"])
    print("Test streaming URL:", f"https://stream.mux.com/{asset_details['playback_ids'][0]}.m3u8")

except Exception as e:
    print("Error in test: ", str(e))

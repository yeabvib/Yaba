async with httpx.AsyncClient() as client:
    try:
        response = await client.post(f"{CHAPA_API_URL}/transaction/initialize", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            return data["data"]["checkout_url"], tx_ref
    except httpx.HTTPStatusError as e:
        print(f"Chapa API Error: {e.response.text}")
return None, None
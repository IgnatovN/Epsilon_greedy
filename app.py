from random import choice
import uvicorn
from fastapi import FastAPI
import numpy as np

app = FastAPI()

click_counter = 0

click_stat = {}
offer_stat = {}


@app.on_event("startup")
def startup_event():
    """Reset statistics"""
    global click_stat, offer_stat
    click_stat, offer_stat = {}, {}


@app.get("/sample/")
def sample(click_id: int, offer_ids: str) -> dict:
    """Greedy sampling"""
    global click_counter, click_stat, offer_stat

    # Parse offer IDs
    offer_ids = [int(offer) for offer in offer_ids.split(",")]

    # upgrade clicks number
    click_counter += 1

    # Sample top offer ID
    # Warm start
    if click_counter <= 100:
        offer_id = choice(offer_ids)

    # Upper Confidence Bound
    else:
        max_ucb = 0
        top_offer = None

        for offer_id in offer_ids:
            if offer_id in offer_stat:

                avg_reward = offer_stat[offer_id]['reward'] / offer_stat[offer_id]['clicks']
                offer_clicks = offer_stat[offer_id]['clicks']

                ucb = avg_reward + np.sqrt(2 * np.log(click_counter) / offer_clicks)

                if ucb > max_ucb:
                    max_ucb, top_offer = ucb, offer_id

            if top_offer:
                offer_id = top_offer
            else:
                offer_id = offer_ids[0]

    # update statistics
    click_stat[click_id] = offer_id

    if offer_id not in offer_stat:
        offer_stat[offer_id] = {'clicks': 1, 'reward': 0, 'conversions': 0}
    else:
        offer_stat[offer_id]['clicks'] += 1

    # Prepare response
    response = {
        "click_id": click_id,
        "offer_id": offer_id,
    }

    return response


@app.put("/feedback/")
def feedback(click_id: int, reward: float) -> dict:
    """Get feedback for particular click"""
    global click_stat, offer_stat
    # Response body consists of click ID
    # and accepted click status (True/False)
    conversion = bool(reward)

    offer_id = click_stat[click_id]

    if offer_id not in offer_stat:
        offer_stat[offer_id] = {'clicks': 1, 'reward': reward, 'conversions': conversion}
    else:
        offer_stat[offer_id]['reward'] += reward
        offer_stat[offer_id]['conversions'] += conversion

    response = {
        "click_id": click_id,
        "offer_id": offer_id,
        "is_conversion": conversion,
        "reward": reward
    }
    return response


@app.get("/offer_ids/{offer_id}/stats/")
def stats(offer_id: int) -> dict:
    """Return offer's statistics"""
    global offer_stat

    if offer_id in offer_stat:

        clicks = offer_stat[offer_id]['clicks']
        conversions = offer_stat[offer_id]['conversions']
        reward = offer_stat[offer_id]['reward']
        conv_rate = conversions / clicks
        rpc = reward / clicks

    else:

        clicks = 0
        conversions = 0
        reward = 0
        conv_rate = 0
        rpc = 0

    response = {
        "offer_id": offer_id,
        "clicks": clicks,
        "conversions": conversions,
        "reward": reward,
        "cr": conv_rate,
        "rpc": rpc,
    }
    return response


def main() -> None:
    """Run application"""
    uvicorn.run("app:app", host="localhost")


if __name__ == "__main__":
    main()

## Troth's bot

Hackathon winner for [Starknet Winter hackathon](https://taikai.network/starkware/hackathons/starknet-winter-hackathon/winners?token=NLPU3RY9KA6U7AQO) (3rd place general, 1st place Giza track) 

This project was developed for the Giza's track of the Starknet Winter hackathon. The idea was to demonstrate how Giza actions could be used for Telegram bots and other chat applications, so that async functions (i.e. actions) could process incoming messages to a bot. The bot can be accessed at https://t.me/giza_sentiment_bot.

The use case we explored here was a standard one, namely ETH price prediction. We used the Giza's Dataset loader for fetching token prices, combined with a ![Prophet](https://facebook.github.io/prophet/) model to generate a forecast for the next 5 days. This forecast is produced via a Giza action and finally sent to the user as a message over Telegram.

We believe this use-case is innovative since it demonstrates different ways in which ZKML can be packaged and delivered to users, this time in a more social way.

We also briefly discuss our choice of ML model for forecasting. We used Prophet because it offers fast training and inference with reasonable results. However, it's worth mentioning that other models (particularly tsai or LagLlama) are very promising, but we note that the large model size might prove troublesome for ZK verification with Cairo.

## How we would have expanded this with more time

The verifiability part of the model could not be achieved due to difficulties related to a. converting the Prophet model into the ONNX format and b. converting from ONNX to the Cairo format (we expect the model to have a large size hence be non-trivial to convert). It would be great to continue working on this conversion and allowing more models to be verifiable on-chain.

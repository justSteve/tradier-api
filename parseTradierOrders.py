#parseTradierOrders.py

import os
import argparse
import config
import requests
import json
import sys
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import logging
import config_logging
from models.Strade import Strade
from models.TradierOrder import TradierOrder
from models.TradierLeg import TradierLeg
from utils import decode_occ_symbol, encode_occ_symbol


# Set up logging
config_logging.setup(__file__)
logger = logging.getLogger(__name__)


def load_orders_from_file(filename='orders.json'):
    orders = []
    with open(filename, "r") as file:
        try:
            data = json.load(file)
            orders_data = data.get('orders', {}).get('order', [])
            if not orders_data:
                logger.error("No orders found in orders.json or incorrect structure.")
                return []  # Return an empty list
        except json.JSONDecodeError:
            logger.error("Error decoding JSON from orders.json.")
            return []
    
    for order_data in orders_data:
        order_id = order_data.get("id", "UNKNOWN")

        try:
            TradierOrder.validate_order(order_data)
            order = TradierOrder.from_dict(order_data)
        
            try:
                order = TradierOrder.from_dict(order_data)
                
                # Process each leg and attach it to the order
                for leg_data in order_data.get('leg', []):
                    leg = TradierLeg.from_dict(leg_data)
                    leg.parent_id = order_id  # Set the parent_id attribute for each leg
                    order.add_leg(leg)
                
                orders.append(order)
            except ValueError as e:
                logger.error(f"Invalid data for order with ID: {order_id}. Error: {e}")
            except Exception as e:    
                logger.warning(f"Unexpected error processing order with ID: {order_id}. Error: {str(e)}")  
        except ValueError as e:
              logger.error(f"Invalid ID: {order_id}. Error: {e}")
            
            
    return orders



def parseTradierToStrade(orders, existing_strades=None):
    if existing_strades is None:
        existing_strades = []

    for order in orders:
        try:
            # Find the center strike leg by looking for 'sell_to_open'
            center_strike_leg = next((leg for leg in order.legs if leg.side == 'sell_to_open'), None)
            
            if center_strike_leg is None:
                for leg in order.legs:
                    logger.info(f"No center strike leg found for order with ID: {order.order_id}. Leg: {leg.__dict__} ")
                continue  # Skip this order
            
            logger.info(f"OrderID has: {order.order_id} Center strike leg: {center_strike_leg.__dict__}")
            decoded_symbol = decode_occ_symbol(center_strike_leg.option_symbol)
            
            strike_str = decoded_symbol["strike"]
            type_str = decoded_symbol["type"]
            
            matching_strade = next((s for s in existing_strades if s.strike == strike_str and s.type == type_str), None)
            
            if matching_strade:
                matching_strade.add_order(order)
            else:
                new_strade = Strade(order.order_id, strike_str, type_str, None)
                new_strade.add_order(order)
                existing_strades.append(new_strade)
                
        except Exception as e:
            logger.warning(f"Error in: {order.order_id}. Error: {str(e)}")

        for strade in existing_strades:
            print(f"Existing Strade: {strade.id}")
    return existing_strades



if __name__ == "__main__":
    try:
        tradier_orders = load_orders_from_file()
    except Exception as e:
        logger.error(f"Error loading orders from file: {str(e)}")
        tradier_orders = []

    try:
        butterflies = parseTradierToStrade(tradier_orders)
        logger.info(f"Successfully parsed {len(butterflies)} butterflies.")
    except Exception as e:
        logger.error(f"Error parsing Tradier orders to Strade: {str(e)}")
        butterflies = []

    try:
        for butterfly in butterflies:
            logger.info(f"Processed butterfly with order ID: {butterfly.order_id}")
    except Exception as e:
        logger.error(f"Error logging processed butterflies: {str(e)}")



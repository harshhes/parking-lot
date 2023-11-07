import random
import json
import logging
import boto3
from botocore.exceptions import ClientError

from boto_config import BUCKET_NAME, aws_access_key_id, aws_secret_access_key, aws_region

class ParkingLot:

    def __init__(self, sqr_foot_size, parking_spot_size=(8,12)):
        self.num_parking_spots = sqr_foot_size // (parking_spot_size[0] * parking_spot_size[1])
        self.parking_lot = [None] * self.num_parking_spots

    def is_spot_empty(self, parking_spot):
        return self.parking_lot[parking_spot] is None
    
    def park_car(self, car, parking_spot):
        self.parking_lot[parking_spot] = car

    def map_cars_to_spots(self):
        mapping = {}
        for spot, car in enumerate(self.parking_lot):
            if car is not None:
                mapping[spot] = car.license_plate
        return mapping

    

class Car:

    def __init__(self, license_plate):
        self.license_plate =  license_plate 

    def __str__(self):
        return self.license_plate
    
    def park(self, parking_lot, parking_spot):
        if parking_lot.is_spot_empty(parking_spot):
            parking_lot.park_car(self, parking_spot)
            return f"Car with license plate {self.license_plate} parked successfully in spot #{parking_spot}"
        else:
            return f"Car with license plate {self.license_plate} couldn't park in spot #{parking_spot}"


def main():

    parking_lot = ParkingLot(int(input("Please Enter size for Parking lot: ")))

    # CAR3841PA
    cars = [
        Car(f"CAR{random.randint(3000, 3999)}"    
        + chr(random.randint(ord('A'), ord('Z')))
        + chr(random.randint(ord('A'), ord('Z'))))
        for _ in range(1, 21)
    ]  


    while cars and None in parking_lot.parking_lot:
        car = random.choice(cars)
        spot = random.randint(0, parking_lot.num_parking_spots - 1)
        result = car.park(parking_lot, spot)
        print(result)
        if "parked successfully" in result:
            cars.remove(car)
            
    # mapping the cars to parking spots   
    mapping = parking_lot.map_cars_to_spots()
    
    with open("parking_mapping.json", "w") as f:
        json.dump(mapping, f)

    
    # Uploading the mapping JSON file to S3 bucket
    session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)
    s3 = session.client('s3')
    bucket_name = BUCKET_NAME
    try:
        response = s3.upload_file('parking_mapping.json', bucket_name, 'parking_mapping.json')
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    
if __name__ == "__main__":
    main()
# "Satellite System" Project

The project's objective is to model satellite movements over the Earth. It allows for adding satellite groups to the model or calculating the percentage of the Earth's area covered by satellites of a given group at a given time.

This involves approximate calculations. Uber's h3 library is used, which divides the Earth into regular hexagons of a given size. We consider a satellite to cover a hexagon if its center is within the satellite's field of view. The program counts the number of covered hexagons of a given size and divides this by the total number of hexagons of that size. This is how coverage is calculated.

## How to work with the program

### Installation
Clone the repository and switch to the main branch
```
git clone -b main https://github.com/volkovlr/Satellite-system
```

Then create a virtual environment in the project folder
```
python -m venv venv
source venv/bin/activate  # Linux / macOS
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

After that, run the project
```
python -m satellite_system.main
```

### Comands
#### Creating a group
Below is an example of creating a satellite constellation:
```
add_group 500 45 30 4 16 3 0 2026-01-15 14:30:45.123456 20
```
That is, the grouping is set by nine parameters that come after "add_group", here they are in the order in which they need to be written in the console:

1. The height of each orbit above the Earth (in kilometers)
2. The inclination of each orbit (in degrees)
3. The longitude of the ascending node for the first orbit (in degrees)
4. The number of orbits in the grouping
5. The number of satellites in the grouping (it is assumed that it is divided by the number of orbits)
6. Phase shift between neighboring orbits (in degrees)
7. The phase of the first satellite in the first orbit (in degrees)
8. Time of grouping creation (in datetime.datetime format)
9. Half of the viewing angle of each satellite (in degrees)

After that, the group will be assigned a number. You will learn about this from a message like this:
```
[2025-12-21 15:53:52] [RESULT] Added a group with a number: 1054
```

#### Calculating coverage
To calculate the coverage of a certain grouping at a given time, the command is written as follows (example):
```
calculate_coverage 1054 4 2026-02-15 14:30:45.123456
```
After "calculate_coverage" the grouping number, resolution (as the resolution increases, the accuracy of the calculation increases, but the resolution cannot be greater than six) and the time at which the coverage should be calculated.

Table of correspondence between resolutions and side lengths of regular hexagons into which the Earth is divided in calculations (information taken using the h3 library):

| Resolution | Side lenght, km |
|--------|------------|
| 1 | 483 |
| 2 | 183 |
| 3 | 69 |
| 4 | 26 |
| 5 | 9,9 |
| 6 | 3,7 |

#### Shutdown
For the end of the work write "exit"


### A complete example of working with the program
```
Enter the command
add_group 500 45 30 4 16 3 0 2026-01-15 14:30:45.123456 20
[2025-12-29 23:15:27] [RESULT] Added a group with a number: 2703
calculate_coverage 2703 4 2026-02-15 14:30:45.123456
[2025-12-29 23:16:01] [RESULT] Coverage of group 2703 is 0.177%
exit
```

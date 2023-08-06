# Sunscreen

Get today's ultraviolet (UV) index forecast for your zipcode

## Install
Using pipsi is recommended, since this is a standalone application.

```
# if necessary
$ pip install pipsi
$ pipsi install sunscreen
```

## Usage

To use sunscreen after installation, just type `sunscreen`:

```bash
▶ sunscreen
Welcome to sunscreen! 🌞 📊
Enter US zipcode [78701]:
Retrieving today's UV data...
Time             UV level
0900 **          2
1000 ****        4
1100 *******     7
1200 *********   9
1300 *********** 11
1400 *********** 11
1500 *********   9
1600 *******     7
1700 ****        4
1800 **          2
```

By default it will use the most recent zip code. If one can't be found, you'll
need to include one on the first run.


# imdb-report-api

An IMDB report generator API implemented with Flask. It processes the data of an IMDB account and gives you relevant information about it.


## API Reference

#### Pick an unwatched movie given a list of movies.

```http
  POST /movies/picku
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `file` | `csv file` | **Required**. The file with the list of movies you want to pick from |

#### Calculate the amount of time spent watching movies given a list of ratings.
It returns the total minutes, and in days, hours and minutes.

```http
  POST /movies/time
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `file`      | `csv file` | **Required**. The file with the list of ratings |

#### Get watched movies by release year.
It returns the title of the movies watched, separated by release year.

```http
  POST /movies/yreleased
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `file`      | `csv file` | **Required**. The file with the list of ratings |

#### Get watched movies by rate year.
It returns the title of the movies watched, separated by the year you rated it.

```http
  POST /movies/yrated
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `file`      | `csv file` | **Required**. The file with the list of ratings |

#### Get most watched movie genres.
It returns a list of watched genres and how many movies the user has seen from each one, sorted by that value descending. It also works with combination of genres, like "Drama & Thriller".

```http
  POST /movies/genre/mw
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `file`      | `csv file` | **Required**. The file with the list of ratings |

#### Get most favorite movie genres.
It returns a list with user's favorite genres, sorted by favoritism descending. It also works with combination of genres, like "Drama & Thriller".

```http
  POST /movies/genre/fav
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `file`      | `csv file` | **Required**. The file with the list of ratings |

This works by having a value to track how much the user likes a genre, wich is obtained by adding the rate the user has given to a movie and multiplying that for a constant. The following table shows the constants for a given rate.

| Rate     | Constant|
| :-------- | :------- |
| `1`      | `-60` |
| `2`      | `-50` |
| `3`      | `-40` |
| `4`      | `-30` |
| `5`      | `-20` |
| `6`      | `0` |
| `7`      | `20` |
| `8`      | `80` |
| `9`      | `100` |
| `10`      | `200` |


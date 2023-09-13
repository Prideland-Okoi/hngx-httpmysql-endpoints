# Student Management API Documentation

This documentation provides information on how to use the Student Management API endpoints.

## Endpoints

### Create a New Student (HTTP POST)

- **URL:** `/api`
- **Method:** `POST`
- **Request Body:** JSON
  - `name` (string, required): Student's name.
  - `track` (string, required): Student's track.

* Example Request:

```
{
  "name": "John Doe",
  "track": "Computer Science"
}
```

- Example Response (Success):

````{
  "message": "studentlog created successfully",
  "student log": {
    "id": 1,
    "name": "John Doe",
    "track": "Computer Science"
  }
}```

### Get a Student by Name (HTTP GET)

- **URL:** `/api/<name>`
- **Method:** `GET`

* Example Response (Success):

```{
  "student info": {
    "id": 1,
    "name": "John Doe",
    "track": "Computer Science"
  }
}```

### Update a Student by Name (HTTP PUT)

- ** URL:** `/api/<name>`
- **Method:** `PUT`
- **Request Body:** JSON
    *name* (string, required): New name for the student.
    *track* (string, required): New track for the student.

* Example Request:

```{
  "name": "Jane Smith",
  "track": "Mathematics"
}```

* Example Response (Success):

`{
  "message": "student updated successfully",
  "student info": "Jane Smith"
}`

### Delete a Student by Name (HTTP DELETE)

- **URL:** `/api/<name>`
- *Method:* DELETE
* Example Response (Success):

```{
  "message": "student deleted successfully",
  "data": {
    "name": "Jane Smith"
  }
}```

## Error Handling

If an invalid request is made or an error occurs, the API will respond with an error message and an appropriate status code.
For more details on how to use each endpoint, refer to the Usage section in the README.md file.
````

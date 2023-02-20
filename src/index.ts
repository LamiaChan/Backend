import express, { Express } from "express";
import dotenv from 'dotenv';
import bodyParser from "body-parser";

import { connectToDatabase } from "./database.service";
import { Router } from "./routes/router";

dotenv.config();

const app: Express = express()
const port = process.env.PORT ? process.env.PORT : ''

app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

app.listen(port, () => {
  connectToDatabase()
  Router('v1', app)
  console.log('lamiachan backend api startup! http://localhost:' + port)
})
import express, { Express } from "express";
import dotenv from 'dotenv';

import { connectToDatabase } from "./database.service";
import {Router as v1} from "./routes/router";

dotenv.config();

const app: Express = express()
const port = process.env.PORT ? process.env.PORT : ''

app.listen(port, () => {
  connectToDatabase()
  v1(app)
  console.log('lamiachan backend api startup! http://localhost:' + port)
})
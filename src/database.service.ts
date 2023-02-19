import * as mongoDB from "mongodb";
import * as dotenv from "dotenv";

dotenv.config();

export const collections: { manga?: mongoDB.Collection } = {}

const db_url = process.env.DB_URL ? process.env.DB_URL : ''
const db_name = process.env.DB_NAME ? process.env.DB_NAME : ''
const collection_manga = process.env.DB_MANGA_COLLECTION_NAME ? process.env.DB_MANGA_COLLECTION_NAME : ''

export async function connectToDatabase () {
  dotenv.config();
  const client: mongoDB.MongoClient = new mongoDB.MongoClient(db_url)
  await client.connect()
  const db: mongoDB.Db = client.db(db_name)
  const gamesCollection: mongoDB.Collection = db.collection(collection_manga)
  collections.manga = gamesCollection
     
  console.log(`Connected to database: ${db.databaseName} and collections: ${gamesCollection.collectionName}`);
}
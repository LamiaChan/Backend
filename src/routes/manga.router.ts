import { collections } from "../database.service"
import { Express, Request, Response } from "express"
import { ObjectId } from "mongodb"
import MangaModule from "../modules/manga.module"

export function Manga(apiVersion: string, app: Express) {
  app.get(`/api/${apiVersion}/manga`, async (req: Request, res: Response) => {
    try {
      if (collections.manga) {
        const manga = (await collections.manga.find({}).toArray()) as unknown as MangaModule[]
        res.status(200).send(manga);
      }
    } catch (error) {
      res.status(500).send(error);
    }
  })

  app.get(`/api/${apiVersion}/manga/:id`, async (req: Request, res: Response) => {
    const id = req?.params?.id;
    try {
      if (collections.manga) {
        const query = { _id: new ObjectId(id) };
        const manga = (await collections.manga.findOne(query)) as unknown as MangaModule
        res.status(200).send(manga);
      }
    } catch (error) {
      res.status(500).send(error);
    }
  })

  app.post(`/api/${apiVersion}/manga`, async (req: Request, res: Response) => {
    try {
      const newManga: MangaModule = req.body as MangaModule
      if (collections.manga) {
        const result = await collections.manga.insertOne(newManga)
        result
          ? res.status(201).send(`Successfully created a new manga with id ${result.insertedId}`)
          : res.status(500).send("Failed to create a new manga.");
      }
    } catch (error) {
        console.error(error);
        res.status(400).send(error);
    }
  })

  app.put(`/api/${apiVersion}/manga/:id`, async (req: Request, res: Response) => {
    const id = req?.params?.id;
    try {
      const updateManga: MangaModule = req.body as MangaModule
      const query = {_id: new ObjectId(id)}
      if (collections.manga) {
        const result = await collections.manga.updateOne(query, {$set: updateManga})
        result
          ? res.status(201).send(`Successfully updated manga with id ${id}`)
          : res.status(500).send(`Manga with id: ${id} not updated`)
      }
    } catch (error) {
        console.error(error);
        res.status(400).send(error);
    }
  })

  app.delete(`/api/${apiVersion}/manga/:id`, async (req: Request, res: Response) => {
    const id = req?.params?.id;

    try {
        const query = { _id: new ObjectId(id) };
        if (collections.manga) {
          const result = await collections.manga.deleteOne(query);
          if (result && result.deletedCount) {
              res.status(202).send(`Successfully removed manga with id ${id}`);
          } else if (!result) {
              res.status(400).send(`Failed to remove manga with id ${id}`);
          } else if (!result.deletedCount) {
              res.status(404).send(`Manga with id ${id} does not exist`);
          }
        }
    } catch (error) {
        console.error(error);
        res.status(400).send(error);
    }
  })
}
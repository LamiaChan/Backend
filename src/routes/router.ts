import { Manga } from "./manga.router"
import { Express } from "express"

export function Router(app: Express) {
  Manga(app)
}
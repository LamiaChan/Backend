import { Manga } from "./manga.router"
import { Express } from "express"

export function Router(routerVersion: string, app: Express) {
  Manga(routerVersion, app)
}
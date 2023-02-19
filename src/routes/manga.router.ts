import { Express, Request, Response } from "express"

export function Manga(app: Express) {
  app.post('/api/manga', (req: Request, res: Response) => {
    res.send('manga post')
  })
  app.get('/api/manga/:id', (req: Request, res: Response) => {
    res.send('manga get')
  })
  app.put('/api/manga/:id', (req: Request, res: Response) => {
    res.send('manga put')
  })
  app.delete('/api/manga/:id', (req: Request, res: Response) => {
    res.send('manga put')
  })
}
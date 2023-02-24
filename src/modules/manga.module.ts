import { ObjectId } from "mongodb";
import ChapterModule from "./chapter.module";

export default class MangaModule {
  constructor(
    public name: string, 
    public altName: string, 
    public type: string, 
    public format: string, 
    public author: string, 
    public releaseDate: string, 
    public drawer: string, 
    public ageRating: string, 
    public imageUrl: string, 
    public detailImageUrl: string, 
    public tags: string[],
    public chapters: ChapterModule[],
    public id?: ObjectId
  ) {}
}
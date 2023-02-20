import { ObjectId } from "mongodb";

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
    public image: string, 
    public detailImage: string, 
    public tags: string[],
    public id?: ObjectId
  ) {}
}
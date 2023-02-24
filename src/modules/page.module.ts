import { ObjectId } from "mongodb";

export default class PageModule {
  constructor(
    public imageUrl: string,
    public number: number, 
    public id?: ObjectId
  ) {}
}
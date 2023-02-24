import { ObjectId } from "mongodb";
import PageModule from "./page.module";

export default class ChapterModule {
  constructor(
    public name: string, 
    public dateUploaded: Date,
    public dateRelease: Date,
    public pages: PageModule[],
    public id?: ObjectId
  ) {}
}
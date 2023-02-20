import { ObjectId } from "mongodb";

export default class MangaModule {
  constructor(public name: string, public id?: ObjectId) {}
}
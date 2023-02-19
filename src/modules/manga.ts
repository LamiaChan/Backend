import { ObjectId } from "mongodb";

export default class Manga {
  constructor(public name: string, public id?: ObjectId) {}
}
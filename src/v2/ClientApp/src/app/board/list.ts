import { Card } from './card';

export interface List {
  id: string;
  name: string;
  cards: Card[];
  cardsSelected: number;
  color: string;
}

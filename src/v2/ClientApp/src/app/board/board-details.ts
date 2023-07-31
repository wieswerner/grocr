import { Board } from '../boards/board';
import { List } from './list';

export interface BoardDetails extends Board {
  lists: List[];
}

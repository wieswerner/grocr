import { Component } from '@angular/core';
import { Board } from '../boards/board';

@Component({
  selector: 'app-board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.css'],
})
export class BoardComponent {
  board: Board | null = null;
}

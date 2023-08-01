import { Component, Inject, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BoardDetails } from './board-details';
import { ActivatedRoute } from '@angular/router';
import { Card } from './card';
import { List } from './list';

@Component({
  selector: 'app-board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.css'],
})
export class BoardComponent implements OnInit {
  board: BoardDetails | null = null;
  cards: Card[] = [];
  colors: string[] = ['basic', 'primary', 'accent', 'warn'];

  constructor(
    private readonly http: HttpClient,
    @Inject('BASE_URL') private readonly baseUrl: string,
    private readonly activatedRoute: ActivatedRoute
  ) {}

  ngOnInit(): void {
    const boardId = this.activatedRoute.snapshot.paramMap.get('id');

    this.http
      .get<BoardDetails>(this.baseUrl + 'api/trello/boards/' + boardId)
      .subscribe({
        next: (result) => {
          this.board = result;
          let colorIndex = 0;

          this.board.lists.forEach((list) => {
            list.cardsSelected = 0;
            list.color = this.colors[colorIndex];

            list.cards.forEach((card) => {
              card.listName = list.name;
              card.color = list.color;
            });

            this.cards = this.cards.concat(list.cards);
            colorIndex++;
          });
        },
        error: (error) => console.error(error),
      });
  }

  toggleList(list: List) {
    this.cards
      .filter((card) => card.listName == list.name)
      .forEach((card) => (card.isSelected = !card.isSelected));
  }

  toggleCard(cardId: string): void {
    for (let card of this.cards) {
      if (card.id === cardId) {
        card.isSelected = !card.isSelected;
        return;
      }
    }
  }
}

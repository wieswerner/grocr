import { Component, Inject, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BoardDetails } from './board-details';
import { ActivatedRoute } from '@angular/router';
import { Card } from './card';
import { List } from './list';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.css'],
})
export class BoardComponent implements OnInit {
  board: BoardDetails | null = null;
  cards: Card[] = [];
  displayedCards: Card[] = [];
  colors: string[] = ['basic', 'primary', 'accent', 'warn'];
  searchFormControl = new FormControl('');

  constructor(
    private readonly http: HttpClient,
    @Inject('BASE_URL') private readonly baseUrl: string,
    private readonly activatedRoute: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.setupSearch();
    this.getCards();
  }

  getCards() {
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

          this.displayedCards = this.cards;
        },
        error: (error) => console.error(error),
      });
  }

  setupSearch() {
    this.searchFormControl.valueChanges.subscribe({
      next: (value) => {
        if (value) {
          this.displayedCards = this.cards.filter(
            (card) => card.name.toLowerCase().indexOf(value.toLowerCase()) != -1
          );
        } else {
          this.displayedCards = this.cards;
        }
      },
    });
  }

  toggleList(list: List) {
    this.cards
      .filter((card) => card.listName == list.name)
      .forEach((card) => (card.isSelected = !card.isSelected));
  }
}

import { Component, Inject, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BoardDetails } from './board-details';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.css'],
})
export class BoardComponent implements OnInit {
  board: BoardDetails | null = null;

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
        next: (result) => (this.board = result),
        error: (error) => console.error(error),
      });
  }
}

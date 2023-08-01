import { HttpClient } from '@angular/common/http';
import { Component, Inject, OnInit } from '@angular/core';
import { Board } from './board';
import { Router } from '@angular/router';

@Component({
  selector: 'app-boards',
  templateUrl: './boards.component.html',
  styleUrls: ['./boards.component.css'],
})
export class BoardsComponent implements OnInit {
  boards: Board[] = [];

  constructor(
    private readonly http: HttpClient,
    @Inject('BASE_URL') private readonly baseUrl: string,
    private readonly router: Router
  ) {}

  ngOnInit(): void {
    this.http.get<Board[]>(this.baseUrl + 'api/trello/boards').subscribe({
      next: (result) => (this.boards = result),
      error: (error) => console.error(error),
    });
  }

  selectBoard(boardId: string): void {
    this.router.navigate(['/sync-overview', boardId]);
  }
}

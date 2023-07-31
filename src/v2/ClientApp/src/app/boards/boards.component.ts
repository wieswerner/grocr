import { HttpClient } from '@angular/common/http';
import { Component, Inject, OnInit } from '@angular/core';
import { Board } from './board';

@Component({
  selector: 'app-boards',
  templateUrl: './boards.component.html',
  styleUrls: ['./boards.component.css'],
})
export class BoardsComponent implements OnInit {
  boards: Board[] = [];

  constructor(
    readonly http: HttpClient,
    @Inject('BASE_URL') readonly baseUrl: string
  ) {}

  ngOnInit(): void {
    this.http.get<Board[]>(this.baseUrl + 'api/trello/boards').subscribe({
      next: (result) => (this.boards = result),
      error: (error) => console.error(error),
    });
  }
}

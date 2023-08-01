import { Component, Inject, ViewChild } from '@angular/core';
import { BoardComponent } from '../board/board.component';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { Ingredient } from '../ingredients/ingredient';
import { IngredientsComponent } from '../ingredients/ingredients.component';

@Component({
  selector: 'app-sync-overview',
  templateUrl: './sync-overview.component.html',
  styleUrls: ['./sync-overview.component.css'],
})
export class SyncOverviewComponent {
  @ViewChild(BoardComponent) boardComponent!: BoardComponent;
  @ViewChild(IngredientsComponent) ingredientsComponent!: IngredientsComponent;

  constructor(
    private readonly http: HttpClient,
    @Inject('BASE_URL') private readonly baseUrl: string,
    private readonly activatedRoute: ActivatedRoute
  ) {}

  getIngredients(event: string) {
    let ingredients: Ingredient[] = [];

    if (event === 'test') {
      ingredients.push({ name: 'Salt' });
      ingredients.push({ name: 'Pepper' });
      ingredients.push({ name: 'Sausage' });
      ingredients.push({ name: 'Bacon' });

      this.ingredientsComponent.populateIngredients(ingredients);
    } else {
      const selectedRecipes = this.boardComponent.getSelectedRecipes();
      if (selectedRecipes.length === 0) return;

      const boardId = this.activatedRoute.snapshot.paramMap.get('id');
      const ids = selectedRecipes.map((recipe) => recipe.id).join(',');

      this.http
        .get<Ingredient[]>(
          `${this.baseUrl}api/openai/boards/${boardId}/ingredients/?ids=${ids}`
        )
        .subscribe({
          next: (result) =>
            this.ingredientsComponent.populateIngredients(result),
          error: (error) => console.error(error),
        });
    }
  }
}

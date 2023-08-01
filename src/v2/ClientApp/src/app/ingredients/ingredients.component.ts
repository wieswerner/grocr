import { Component, EventEmitter, Output } from '@angular/core';
import { Ingredient } from './ingredient';

@Component({
  selector: 'app-ingredients',
  templateUrl: './ingredients.component.html',
  styleUrls: ['./ingredients.component.css'],
})
export class IngredientsComponent {
  @Output() getIngredients = new EventEmitter<string>();
  ingredients: Ingredient[] = [];

  onGetIngredients() {
    this.getIngredients.emit('live');
  }

  onTestIngredients() {
    this.getIngredients.emit('test');
  }

  populateIngredients(ingredients: Ingredient[]) {
    this.ingredients = ingredients;
  }

  remove(ingredient: Ingredient) {
    let index = this.ingredients.findIndex(
      (item) => item.name === ingredient.name
    );

    if (index !== -1) {
      this.ingredients.splice(index, 1);
    }
  }
}

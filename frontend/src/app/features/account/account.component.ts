import {Component, inject} from '@angular/core';
import {UserService} from "@services/user.service";
import {AuthService} from "@services/auth.service";

@Component({
  selector: 'app-account',
  standalone: true,
  imports: [],
  templateUrl: './account.component.html',
  styleUrl: './account.component.css'
})
export class AccountComponent {
  userService: UserService = inject(UserService);
  authService: AuthService = inject(AuthService);
  userId: string | null = null;

  constructor() {
  }

  getUser() {
    this.userId = this.authService.getUserId();
    if (this.userId) {
      this.userService.getUser(this.userId).subscribe(user => {
        console.log(user.id);
        console.log(user.integrations);
      });
    } else {
        console.log("No user logged in.");
    }
  }
}

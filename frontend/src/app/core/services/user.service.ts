import {inject, Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {environment} from "@environments/environment";
import {map, Observable} from "rxjs";
import {User} from "@models/user";

/**
 * Responsible for retrieving and modifying User data
 * through interactions with the Gigs API.
 */
@Injectable({
    providedIn: 'root'
})
export class UserService {
    private http = inject(HttpClient);

    getUser(userId: string): Observable<User> {
        return this.http.get<User>(`${environment.gigsApiUrl}/users/${userId}`).pipe(
            map(data => {
                return new User(data);
            })
        )
    }

}
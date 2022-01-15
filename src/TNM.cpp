#include <TNM.hpp>

void	SDL_ExitWithError(const char *error) {
	SDL_Log("%s: %s\n", error, SDL_GetError());
	exit(1);
}

void	init(SDL_Window **window, SDL_Renderer **renderer) {
	if (SDL_Init(SDL_INIT_VIDEO) != 0)
		SDL_ExitWithError("Error Initialisation SDL");
	if ((*window = SDL_CreateWindow("Test de la négligence sensorielle", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, WINDOW_SIZE_X, WINDOW_SIZE_Y, 0)) == NULL)
		SDL_ExitWithError("Error Window creation");
	if ((*renderer = SDL_CreateRenderer(*window, -1, 0)) == NULL)
		SDL_ExitWithError("Error Renderer creation");
}

void	change_rect_position(SDL_Rect *rect) {
	rect->x = rand() % (WINDOW_SIZE_X - RECT_SIZE);
	rect->y = rand() % (WINDOW_SIZE_Y - RECT_SIZE);
}

void	auto_change_rect_position(SDL_Rect *rect, std::time_t *initial_timestamp) {
	if ((std::time(nullptr) - *initial_timestamp) > TIME_BEFORE_CHANGE) {
		change_rect_position(rect);
		*initial_timestamp = std::time(nullptr);
	}
}

int		main(int ac, char **av) {
	SDL_Window		*window = NULL;
	SDL_Renderer	*renderer = NULL;
	SDL_Event		event;
	bool			stop = false;
	std::time_t		initial_timestamp(std::time(nullptr));

	SDL_Rect		rect;
	rect.x = 390;
	rect.y = 290;
	rect.w = RECT_SIZE;
	rect.h = RECT_SIZE;

	init(&window, &renderer);
	srand(time(0));
	while (!stop) {
		while (SDL_PollEvent(&event)) {
			if (event.type == SDL_QUIT)
				stop = true;
			if (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_ESCAPE)
				stop = true;
			if (event.type == SDL_MOUSEMOTION) {
				/* faire une image statique pour afficher le trajet de la souris
				 * et une image transparente dynamique pour les carres
				SDL_SetRenderDrawColor(renderer, 0xff, 0xff, 0xff, 0xff);
				SDL_RenderDrawPoint(renderer, event.motion.x, event.motion.y);
				SDL_RenderPresent(renderer);
				*/
				if (event.motion.x >= rect.x && event.motion.y >= rect.y &&
						event.motion.x <= rect.x + rect.w && event.motion.y <= rect.y + rect.h) {
					change_rect_position(&rect);
					initial_timestamp = std::time(nullptr);
				}
			}
		}
		SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0xff);
		SDL_RenderClear(renderer);
		SDL_SetRenderDrawColor(renderer, 0xff, 0, 0, 0xff);
		SDL_RenderDrawRect(renderer, &rect);
		SDL_RenderFillRect(renderer, &rect);
		SDL_RenderPresent(renderer);
		auto_change_rect_position(&rect, &initial_timestamp);
	}
	SDL_DestroyRenderer(renderer);
	SDL_DestroyWindow(window);
	SDL_Quit();
	return (0);
}

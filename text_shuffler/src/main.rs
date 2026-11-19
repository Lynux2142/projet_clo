use eframe::egui;
use rand::seq::SliceRandom;

fn shuffle_text(text: &str) -> String {
    let mut rng = rand::rng();

    text.split('\n')
        .map(|line| {
            let mut letters: Vec<char> = line.chars().filter(|c| c.is_alphabetic()).collect();

            letters.shuffle(&mut rng);

            let mut letter_iter = letters.into_iter();
            line.chars()
                .map(|c| {
                    if c.is_alphabetic() {
                        letter_iter.next().unwrap_or(c)
                    } else {
                        c
                    }
                })
                .collect::<String>()
        })
        .collect::<Vec<_>>()
        .join("\n")
}

#[derive(Default)]
struct TextShufflerApp {
    input: String,
    output: String,
}

impl eframe::App for TextShufflerApp {
    fn ui(&mut self, ui: &mut egui::Ui, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ui, |ui| {
            ui.label("Enter text to shuffle:");

            let available_height = ui.available_height();
            let button_and_spacing_height = 44.0;
            let pane_height = ((available_height - button_and_spacing_height) / 2.0).max(60.0);

            egui::ScrollArea::vertical()
                .id_salt("input_scroll")
                .max_height(pane_height)
                .show(ui, |ui| {
                    ui.add_sized(
                        [ui.available_width(), pane_height],
                        egui::TextEdit::multiline(&mut self.input),
                    );
                });

            ui.separator();

            egui::ScrollArea::vertical()
                .id_salt("output_scroll")
                .max_height(pane_height)
                .show(ui, |ui| {
                    ui.add_sized(
                        [ui.available_width(), pane_height],
                        egui::TextEdit::multiline(&mut self.output),
                    );
                });

            ui.add_space(6.0);

            ui.horizontal(|ui| {
                let button_width = 120.0;
                let offset = ((ui.available_width() - button_width) / 2.0).max(0.0);
                ui.add_space(offset);

                if ui
                    .add_sized([button_width, 28.0], egui::Button::new("Shuffle Text"))
                    .clicked()
                {
                    self.output = shuffle_text(&self.input);
                }
            });
        });
    }
}

fn main() -> eframe::Result<()> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default().with_inner_size([600.0, 600.0]),
        ..Default::default()
    };

    eframe::run_native(
        "Text Shuffler",
        options,
        Box::new(|_cc| Ok(Box::new(TextShufflerApp::default()))),
    )
}

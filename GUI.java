import javafx.application.Application;
import javafx.application.Platform;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;

import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.control.Label;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.GridPane;

import javafx.stage.Stage;

public class GUI extends Application{

    private static Label ups = new Label("ups");
    private static Label accelerometer = new Label("Accelerometer");
    private static Label gyroscope = new Label("Gyroscope");
    private static Label proximity = new Label("Proximity");

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Smartphone To Virtuality");

        GridPane grid = new GridPane();

        //Ajout Label Ups
        GridPane.setConstraints(ups, 0, 0);
        grid.getChildren().add(ups);

        //Ajout Label Accelerometres
        GridPane.setConstraints(accelerometer, 0, 1);
        grid.getChildren().add(accelerometer);

        //Ajout Label Gyroscope
        GridPane.setConstraints(gyroscope, 0, 2);
        grid.getChildren().add(gyroscope);

        //Ajout Label proximité
        GridPane.setConstraints(proximity, 0, 3);
        grid.getChildren().add(proximity);

        primaryStage.setScene(new Scene(grid, 500, 500));
        primaryStage.show();
    }

    public static void setUps(int val_){
      Platform.runLater(() -> ups.setText("Update/sec : " + val_));
    }

    public static void setAccelerometer(float x_, float y_, float z_){
      Platform.runLater(() -> accelerometer.setText("Accelerometer : x = " + x_ + " , y = " + y_ + " , z = " + z_));
    }

    public static void setGyroscope(float x_, float y_, float z_){
      Platform.runLater(() -> gyroscope.setText("Gyroscope : x = " + x_ + " , y = " + y_ + " , z = " + z_));
    }

    public static void setProximity(float val_){
      Platform.runLater(() -> proximity.setText("Proximity : " + val_));
    }
}

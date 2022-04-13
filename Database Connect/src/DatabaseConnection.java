import java.sql.*;
//import oracle.jdbc;

public class DatabaseConnection {

    private Connection myConn;
    private Statement myStatement;
    private ResultSet myResults;
    private ResultSetMetaData myResultMetaData;
    private String url = "jdbc:oracle:thin:collingee/46LS3U1A3e8ZnSko0eDeR3up@oracle.cise.ufl.edu:1521:orcl";
    private String testQuery = "SELECT * FROM CLASS";
    private String myQuery;
    private PreparedStatement myPreparedStatement;

    public void getConnection() {
        try {
            this.myConn = DriverManager.getConnection(this.url);
            this.myConn.setAutoCommit(true);
            this.myStatement = this.myConn.createStatement();
        } catch (Exception e) {
            System.out.println("In the error block...why?");
            e.printStackTrace();
        }
    }

    public ResultSet runQuery(String query) {
        try {
            this.myResults = myStatement.executeQuery(query);
            this.myResultMetaData = this.myResults.getMetaData();
            // this.myHeaders = myResultMetaData.getColumnLabel(1);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return this.myResults;
    }

    public void printQueryResults() {
        try {

            // Print out the query value
            System.out.println();
            System.out.println("Query: " + this.myQuery);

            // Print out the headers
            System.out.println();
            for (int i = 1; i <= myResultMetaData.getColumnCount(); i++) {
                System.out.print(myResultMetaData.getColumnLabel(i) + "\t");
            }
            System.out.println();
            while (this.myResults.next()) {
                System.out.println(this.myResults.getString(1) + "\t" + this.myResults.getString(2) + "\t\t"
                        + this.myResults.getString(3));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void closeConnection() {
        try {
            myConn.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void getAllClassValues() {
        this.myQuery = "SELECT * FROM CLASS";
        runQuery(myQuery);
        printQueryResults();
    }

    public void getAllUsersValues() {
        this.myQuery = "SELECT * FROM USERS";
        runQuery(myQuery);
        printQueryResults();
    }

    public void getAllVideoValues() {
        this.myQuery = "SELECT * FROM VIDEO";
        runQuery(myQuery);
        printQueryResults();
    }
    /*
    public void addClassValue() {
        System.out.println("This is where I add a class value");
        //this.myQuery = "INSERT INTO class VALUES ('222', 222, 222, '222');";
        this.myQuery = "INSERT INTO class VALUES (?, ?, ?, ?);";
        /*
        try{
            myConn.setAutoCommit(false);
            this.myPreparedStatement = myConn.prepareStatement(myQuery);
            this.myPreparedStatement.setString(1, "CSCI");
            this.myPreparedStatement.setInt(2, 1234);
            this.myPreparedStatement.setInt(3, 123);
            this.myPreparedStatement.setString(4, "2014");
            this.myPreparedStatement.executeUpdate();
            myConn.commit();
            myConn.setAutoCommit(true);
            getQueryResults(myQuery);
            getAllClassValues();
            printQueryResults();
            
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        runQuery(myQuery);
        getAllClassValues();
        printQueryResults();

    }
    */

// Below are the methods for the functionality

    //Change return type to JSON later
    public String checkUserSignIn(String userName, String password) {
        this.myQuery = "SELECT * FROM USERS WHERE USERNAME = '" + userName + "' AND PASSWORD = '" + password + "';";
        runQuery(myQuery);
        try {
            if (this.myResults.next()) {
                //Return userID
                //Get UserID
                this.myQuery = "SELECT USERID FROM USERS WHERE USERNAME = '" + userName + "' AND PASSWORD = '" + password + "';";
                runQuery(myQuery);

                String returnedUserID = "";
                //Set userID for returninig
                returnedUserID = this.myResults.getString(1);
                return returnedUserID;
            } else {
                return "Failure";
            }
        }catch (Exception e) {
            e.printStackTrace();
            System.out.println("Failure byexception in checkUser");
        }

        printQueryResults();
        return "";
    }


    public static void main(String args[]) {
        DatabaseConnection db = new DatabaseConnection();
        db.getConnection();
        db.getAllClassValues();
        db.getAllUsersValues();
        db.getAllVideoValues();
        //db.addClassValue();
        db.closeConnection();
    }

    // WILL NEED TO DO .COMMIT WHEN PUSHING DATA IN/DELETING DATA FROM DATABASE
}
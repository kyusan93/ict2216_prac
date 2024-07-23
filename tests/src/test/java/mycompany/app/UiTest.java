package com.mycompany.app;

import org.junit.Before;
import org.junit.Test;
import org.junit.After;
import static org.junit.Assert.*;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.htmlunit.HtmlUnitDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class UiTest {
    WebDriver driver; 
    WebDriverWait wait; 
    String url = "http://webapp-test:5000";  // Update this URL if necessary
    String validPassword = "StrongP@ssw0rd";
    String invalidPassword = "short";
    String commonPassword = "password";

    @Before
    public void setUp() { 
        driver = new HtmlUnitDriver(); 
        wait = new WebDriverWait(driver, 10); 
    } 

    @After
    public void tearDown() { 
        driver.quit(); 
    }	 
    
    @Test
    public void testLoginWithValidPassword() throws InterruptedException { 
        driver.get(url);
        wait.until(ExpectedConditions.titleContains("Home Page")); 
        driver.findElement(By.name("password")).sendKeys(validPassword);
        driver.findElement(By.tagName("form")).submit();
        wait.until(ExpectedConditions.titleContains("Welcome Page")); 
        String welcomeText = driver.findElement(By.tagName("body")).getText();
        assertTrue(welcomeText.contains("Your password is: " + validPassword));
    }
    
    @Test
    public void testLoginWithInvalidPassword() throws InterruptedException { 
        driver.get(url);
        wait.until(ExpectedConditions.titleContains("Home Page")); 
        driver.findElement(By.name("password")).sendKeys(invalidPassword);
        driver.findElement(By.tagName("form")).submit();
        wait.until(ExpectedConditions.titleContains("Home Page")); 
        String bodyText = driver.findElement(By.tagName("body")).getText();
        assertTrue(bodyText.contains("Password does not meet requirements or is too common."));
    }
    
    @Test
    public void testLoginWithCommonPassword() throws InterruptedException { 
        driver.get(url);
        wait.until(ExpectedConditions.titleContains("Home Page")); 
        driver.findElement(By.name("password")).sendKeys(commonPassword);
        driver.findElement(By.tagName("form")).submit();
        wait.until(ExpectedConditions.titleContains("Home Page")); 
        String bodyText = driver.findElement(By.tagName("body")).getText();
        assertTrue(bodyText.contains("Password does not meet requirements or is too common."));
    }
}
